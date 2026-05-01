#!/usr/bin/env python3
"""
agent.py — CLI entry point for the Multi-Domain Support Triage Agent.

Reads support tickets from a CSV, runs each through the triage pipeline,
and writes results to an output CSV. Every LLM interaction is also appended
to log.txt so evaluators can audit the full prompt/response trace.

Usage:
    python agent.py                            # default: reads support_tickets/support_tickets.csv
    python agent.py -i <input.csv> -o <out.csv>
    python agent.py --demo                     # runs against sample_support_tickets.csv
    python agent.py --quiet                    # suppresses per-ticket panels
    python agent.py --interactive              # manual single-ticket mode
"""

import argparse
import csv
import os
import sys
import time
from datetime import datetime
from pathlib import Path


# ── .env loader (before any module that reads env vars) ──────────────────────
def _load_dotenv() -> None:
    env_path = Path(__file__).parent.parent / ".env"
    if not env_path.exists():
        env_path = Path(__file__).parent / ".env"
    if env_path.exists():
        for line in env_path.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip())

_load_dotenv()

# ── Rich UI ───────────────────────────────────────────────────────────────────
from rich.console import Console
from rich.panel import Panel
from rich.progress import (BarColumn, Progress, SpinnerColumn,
                           TaskProgressColumn, TextColumn)
from rich.table import Table
from rich.text import Text
from rich import box

# ── Triage pipeline (imported after env is ready) ────────────────────────────
import triage as _triage_module
from triage import triage_ticket

console = Console()

BANNER = """\
╔══════════════════════════════════════════════════════════════╗
║     MULTI-DOMAIN SUPPORT TRIAGE AGENT                       ║
║     Domains: HackerRank · Claude · Visa                     ║
╚══════════════════════════════════════════════════════════════╝"""

_STATUS_STYLE  = {"replied": "green", "escalated": "yellow"}
_RT_STYLE      = {"product_issue": "cyan", "bug": "red",
                  "feature_request": "blue", "invalid": "dim"}


# ── CSV helpers ───────────────────────────────────────────────────────────────
def _read_csv(path: str) -> list[dict]:
    with open(path, newline="", encoding="utf-8") as f:
        return [{k.strip().lower(): (v or "").strip()
                 for k, v in row.items()}
                for row in csv.DictReader(f)]


def _write_csv(path: str, rows: list[dict]) -> None:
    fields = ["issue", "subject", "company", "response", "product_area",
              "status", "request_type", "urgency", "confidence", "citations",
              "justification"]
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)


# ── UI helpers ────────────────────────────────────────────────────────────────
def _print_panel(num: int, subject: str, company: str, result: dict) -> None:
    color = _STATUS_STYLE.get(result["status"], "white")
    rt    = result["request_type"]

    header = Text()
    header.append(f"#{num} ", style="bold white")
    header.append(f"[{company or 'Unknown'}] ", style="bold magenta")
    header.append((subject or "(no subject)")[:60], style="bold")

    urgency    = result.get("urgency", "?")
    confidence = result.get("confidence", 0.0)
    citations  = result.get("citations", [])

    body = Text()
    body.append("STATUS:       ", style="bold")
    body.append(f"{result['status'].upper()}\n", style=f"bold {color}")
    body.append("PRODUCT AREA: ", style="bold")
    body.append(f"{result['product_area']}\n", style="cyan")
    body.append("REQUEST TYPE: ", style="bold")
    body.append(f"{rt}\n", style=_RT_STYLE.get(rt, "white"))
    body.append("URGENCY:      ", style="bold")
    body.append(f"{urgency}/5\n", style="bold yellow")
    body.append("CONFIDENCE:   ", style="bold")
    body.append(f"{confidence:.2f}\n", style="bold green" if confidence >= 0.5 else "bold red")
    if citations:
        body.append("CITATIONS:    ", style="bold")
        body.append(f"{', '.join(citations)}\n", style="dim")
    body.append("\nRESPONSE:\n", style="bold")
    body.append(f"{result['response']}\n", style="white")
    body.append("\nJUSTIFICATION:\n", style="bold dim")
    body.append(result["justification"], style="dim")

    console.print(Panel(body, title=header, border_style=color, padding=(0, 1)))
    console.print()


def _print_summary(results: list[dict]) -> None:
    tbl = Table(title="Triage Summary", box=box.ROUNDED,
                show_lines=True, title_style="bold blue")
    tbl.add_column("#",            style="dim",     width=4)
    tbl.add_column("Company",      style="magenta", width=12)
    tbl.add_column("Subject",                       width=30)
    tbl.add_column("Status",                        width=10)
    tbl.add_column("Product Area",                  width=22)
    tbl.add_column("Request Type",                  width=15)

    for i, r in enumerate(results, 1):
        s = r.get("status", "")
        tbl.add_row(
            str(i),
            r.get("company", ""),
            (r.get("subject") or "(no subject)")[:28],
            Text(s, style=f"bold {_STATUS_STYLE.get(s, 'white')}"),
            r.get("product_area", ""),
            Text(r.get("request_type", ""),
                 style=_RT_STYLE.get(r.get("request_type", ""), "white")),
        )
    console.print(tbl)

    replied   = sum(1 for r in results if r.get("status") == "replied")
    escalated = sum(1 for r in results if r.get("status") == "escalated")
    console.print(
        f"\n  Total: [bold]{len(results)}[/bold]  "
        f"Replied: [green bold]{replied}[/green bold]  "
        f"Escalated: [yellow bold]{escalated}[/yellow bold]\n"
    )


# ── Core processing ───────────────────────────────────────────────────────────
def process_file(input_path: str, output_path: str, log_path: str,
                 verbose: bool = True) -> None:
    rows  = _read_csv(input_path)
    total = len(rows)

    # Wire the log file into the triage module
    _triage_module.LOG_FILE = log_path
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(
            f"\n{'▓' * 72}\n"
            f"RUN STARTED  {datetime.now().isoformat()}\n"
            f"Input  : {input_path}\n"
            f"Output : {output_path}\n"
            f"Model  : {_triage_module.MODEL}  temperature={_triage_module.TEMPERATURE}\n"
            f"{'▓' * 72}\n"
        )

    console.print(f"  Input  : [bold]{input_path}[/bold]  ({total} tickets)")
    console.print(f"  Output : [bold]{output_path}[/bold]")
    console.print(f"  Log    : [bold]{log_path}[/bold]\n")

    output_rows    = []
    summary_rows   = []

    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"),
                  BarColumn(), TaskProgressColumn(),
                  console=console, transient=False) as progress:
        task = progress.add_task("[cyan]Triaging tickets...", total=total)

        for i, row in enumerate(rows, 1):
            issue   = row.get("issue",   "")
            subject = row.get("subject", "")
            company = row.get("company", "")

            progress.update(
                task,
                description=(f"[cyan]Processing #{i}/{total}: "
                             f"{(subject or issue[:30])[:35]}..."),
                advance=0,
            )

            result = triage_ticket(issue, subject, company)

            if verbose:
                progress.stop()
                _print_panel(i, subject, company, result)
                progress.start()

            citations_str = "; ".join(result.get("citations", []))
            output_rows.append({
                "issue":         issue,
                "subject":       subject,
                "company":       company,
                "response":      result["response"],
                "product_area":  result["product_area"],
                "status":        result["status"],
                "request_type":  result["request_type"],
                "urgency":       result.get("urgency", 3),
                "confidence":    result.get("confidence", 0.0),
                "citations":     citations_str,
                "justification": result["justification"],
            })
            summary_rows.append({**result, "company": company, "subject": subject})
            progress.advance(task)

            if i < total:
                time.sleep(0.3)   # stay within Groq free-tier rate limits

    _write_csv(output_path, output_rows)

    console.print("\n" + "─" * 64)
    _print_summary(summary_rows)
    console.print(f"  [green bold]✓[/green bold] CSV  → [bold]{output_path}[/bold]")
    console.print(f"  [green bold]✓[/green bold] Log  → [bold]{log_path}[/bold]\n")


# ── Interactive mode ──────────────────────────────────────────────────────────
def interactive_mode(log_path: str) -> None:
    _triage_module.LOG_FILE = log_path
    console.print("[bold cyan]Interactive Mode[/bold cyan] — Ctrl-C to exit\n")
    num = 0
    while True:
        try:
            console.print("[bold]COMPANY[/bold] (HackerRank / Claude / Visa / None): ", end="")
            company = input().strip()
            console.print("[bold]SUBJECT[/bold] (optional): ", end="")
            subject = input().strip()
            console.print("[bold]ISSUE[/bold] (press Enter twice when done):")
            lines = []
            while True:
                line = input()
                if line == "" and lines and lines[-1] == "":
                    break
                lines.append(line)
            issue = "\n".join(lines).strip()
            if not issue:
                continue
            num += 1
            console.print("\n[dim]Triaging...[/dim]")
            _print_panel(num, subject, company, triage_ticket(issue, subject, company))
        except KeyboardInterrupt:
            console.print("\n[dim]Exiting.[/dim]")
            break


# ── Entry point ───────────────────────────────────────────────────────────────
def main() -> None:
    ap = argparse.ArgumentParser(
        description="Multi-Domain Support Triage Agent (HackerRank · Claude · Visa)"
    )
    ap.add_argument("--input",       "-i", default=None)
    ap.add_argument("--output",      "-o", default=None)
    ap.add_argument("--log",         "-l", default=None,
                    help="Path for log.txt (default: project root)")
    ap.add_argument("--interactive",       action="store_true")
    ap.add_argument("--demo",              action="store_true",
                    help="Run against sample_support_tickets.csv")
    ap.add_argument("--quiet",       "-q", action="store_true",
                    help="Suppress per-ticket panels; show summary only")
    args = ap.parse_args()

    if not os.environ.get("GROQ_API_KEY"):
        console.print("[red bold]Error:[/red bold] GROQ_API_KEY is not set.")
        console.print("  Get a free key at https://console.groq.com")
        console.print("  Then: export GROQ_API_KEY=gsk_...")
        sys.exit(1)

    console.print(BANNER, style="bold blue")
    console.print()

    root = Path(__file__).parent.parent          # support-triage-agent/
    data = root / "support_tickets"
    data.mkdir(exist_ok=True)

    log_path = args.log or str(root / "log.txt")

    if args.interactive:
        interactive_mode(log_path)
        return

    if args.demo:
        in_path  = str(root / "data" / "sample_support_tickets.csv")
        out_path = args.output or str(data / "sample_output.csv")
    else:
        in_path  = args.input  or str(data / "support_tickets.csv")
        out_path = args.output or str(data / "output.csv")

    if not Path(in_path).exists():
        console.print(f"[red bold]Error:[/red bold] Input file not found: {in_path}")
        sys.exit(1)

    console.print(
        f"  [bold blue]Mode   :[/bold blue] {'Demo' if args.demo else 'Production'} | "
        f"[bold blue]Started:[/bold blue] {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    )
    process_file(in_path, out_path, log_path, verbose=not args.quiet)


if __name__ == "__main__":
    main()
