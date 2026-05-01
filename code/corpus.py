"""
Support corpus — pre-scraped from the three official support sites:
  HackerRank : https://support.hackerrank.com/hc/en-us
  Claude     : https://support.claude.com/en/
  Visa       : https://www.visa.co.in/support.html

Each document has:
  id          – unique identifier
  domain      – HackerRank | Claude | Visa
  product_area– canonical support category
  title       – article title
  content     – scraped article body
  keywords    – curated terms for BM25 retrieval
"""

CORPUS: list[dict] = [

    # ──────────────────────────────────────────────────────
    # HACKERRANK
    # ──────────────────────────────────────────────────────
    {
        "id": "hr-001",
        "domain": "HackerRank",
        "product_area": "screen",
        "title": "Test Expiration & Active Status",
        "content": (
            "Tests in HackerRank remain active indefinitely unless a start and end time are set. "
            "Without these, tests do not expire automatically. "
            "To set expiration times, specify a start and end date/time in the test settings. "
            "After expiration: invited candidates cannot access the test; the Invite button is disabled. "
            "To keep the test active indefinitely, clear the start/end fields using the clear icon (X). "
            "Settings → General section → Update Start date & time and End date & time fields."
        ),
        "keywords": ["test active", "test expire", "expiration", "start date", "end date",
                     "invite disabled", "test settings"],
    },
    {
        "id": "hr-002",
        "domain": "HackerRank",
        "product_area": "screen",
        "title": "Test Variants vs. New Tests",
        "content": (
            "Use test variants to adapt a single test to different candidate profiles, such as roles with "
            "different tech stacks (React, Angular, Vue.js). "
            "Variants streamline assessments by showing candidates only relevant sections and generating "
            "role-specific reports. "
            "Advantages: reduces need to manage multiple tests, decreases maintenance while allowing scalable "
            "personalization, ensures candidates are tested on relevant content. "
            "Limitations: a test must have at least two variants to function; you cannot delete a variant "
            "if only two exist; variants without logic are hidden from candidates until logic is added."
        ),
        "keywords": ["variant", "new test", "react", "angular", "vue", "tech stack", "role",
                     "candidate profile"],
    },
    {
        "id": "hr-003",
        "domain": "HackerRank",
        "product_area": "screen",
        "title": "Adding Extra Time / Time Accommodation for Candidates",
        "content": (
            "To add extra time accommodation: "
            "1. Log in to HackerRank for Work. "
            "2. Go to the Tests tab and select the test. "
            "3. Go to the Candidates tab. "
            "4. Select the checkbox next to the candidate(s). "
            "5. Click More → Add Time Accommodation. "
            "6. Enter the accommodation percentage in multiples of five. "
            "7. Click Save. "
            "Time accommodation can also be added before the invite is sent. "
            "Reference: https://support.hackerrank.com/articles/4811403281-adding-extra-time-for-candidates"
        ),
        "keywords": ["extra time", "time accommodation", "reinvite", "accommodation", "disability",
                     "accessibility", "more time"],
    },
    {
        "id": "hr-004",
        "domain": "HackerRank",
        "product_area": "community",
        "title": "Delete HackerRank Account (Google Login)",
        "content": (
            "To delete a HackerRank account created via Google login: "
            "1. Go to the HackerRank login page and click 'Forgot your password?'. "
            "2. Enter the email linked to your Google login and follow instructions to set a new password. "
            "3. Log in using the new password. "
            "4. Click your profile icon → Settings → scroll to Delete Accounts section. "
            "5. Click Delete Account and confirm by entering your password. "
            "Deleting your account permanently removes all data and cannot be undone."
        ),
        "keywords": ["delete account", "google login", "remove account", "close account",
                     "google sign in"],
    },
    {
        "id": "hr-005",
        "domain": "HackerRank",
        "product_area": "screen",
        "title": "Execution Environment – Languages, Memory, Time Limits",
        "content": (
            "HackerRank supports 40+ programming languages. Maximum submission size: 50 KB. "
            "Multithreading supported; CPU time calculated across all threads. "
            "Base OS: Ubuntu LTS. "
            "Languages: C, C++, Java, Python, JavaScript, Go, Rust, and more. "
            "Time limits: 1–12 seconds; memory: typically 512 MB. "
            "Database: MySQL, PostgreSQL, Oracle, MS SQL Server, DB2 (60-second limit, 2–3 GB memory). "
            "Front-End: React, Vue, AngularJS with Node.js v22.16.0. "
            "Back-End: Django, Spring Boot, Rails, .NET, Laravel, Symfony. "
            "Mobile: Swift, Android (Java/Kotlin), React Native, Flutter. "
            "Data Science: Python, R, Julia with ML/statistical libraries (scikit-learn, TensorFlow). "
            "DevOps/Cloud: Ubuntu 24.04 LTS or RHEL 8. "
            "QA Testing: Selenium, Cypress, Playwright."
        ),
        "keywords": ["execution environment", "programming language", "memory limit", "time limit",
                     "python", "java", "javascript", "code execution", "submission size"],
    },
    {
        "id": "hr-006",
        "domain": "HackerRank",
        "product_area": "general",
        "title": "Maintenance Window Notification",
        "content": (
            "HackerRank schedules regular maintenance windows to perform upgrades and improvements. "
            "During maintenance, the platform or specific features may be temporarily unavailable. "
            "Maintenance windows are communicated in advance through official channels. "
            "If you experience unexpected downtime outside a maintenance window, contact support."
        ),
        "keywords": ["maintenance", "downtime", "unavailable", "site down", "not working", "outage",
                     "maintenance window"],
    },
    {
        "id": "hr-007",
        "domain": "HackerRank",
        "product_area": "general",
        "title": "Safelist / Allowlist URLs and IP Addresses",
        "content": (
            "To ensure HackerRank works properly behind firewalls or corporate networks, allowlist: "
            "Domains: *.hackerrank.com, *.hackerranksandbox.com, *.hackerearth.com. "
            "For video interviews, also allowlist Zoom and required video-conferencing domains. "
            "Contact your IT team to configure firewall rules. "
            "Full updated list available in the HackerRank support article on safelisting URLs."
        ),
        "keywords": ["safelist", "allowlist", "whitelist", "firewall", "blocked", "network",
                     "IP address", "URL", "corporate network", "zoom"],
    },
    {
        "id": "hr-008",
        "domain": "HackerRank",
        "product_area": "general",
        "title": "Update or Reset Password",
        "content": (
            "To update your HackerRank password: "
            "1. Go to hackerrank.com/auth/login. "
            "2. Click 'Forgot your password?'. "
            "3. Enter your registered email and click Submit. "
            "4. Check your email for a reset link and set a new password. "
            "If you signed up via Google or LinkedIn SSO, use the Forgot Password flow to set a password first."
        ),
        "keywords": ["password", "reset password", "forgot password", "update password", "login",
                     "sign in"],
    },
    {
        "id": "hr-009",
        "domain": "HackerRank",
        "product_area": "screen",
        "title": "Impersonation Detection in Assessments",
        "content": (
            "HackerRank's impersonation detection uses AI-based proctoring to flag suspicious activity. "
            "System checks: face detection, ID verification (if enabled), browser tab switching, "
            "copy-paste monitoring, and webcam snapshots. "
            "Recruiters can review proctoring reports in the candidate's result page. "
            "Proctoring is configurable — recruiters can enable/disable specific options in test settings."
        ),
        "keywords": ["impersonation", "proctoring", "cheating", "fraud", "webcam", "face detection",
                     "ID verification", "suspicious", "copy paste"],
    },
    {
        "id": "hr-010",
        "domain": "HackerRank",
        "product_area": "screen",
        "title": "Candidate Score Disputes – Policy",
        "content": (
            "HackerRank does not allow support agents or candidates to modify test scores. "
            "Scores are calculated automatically based on code correctness and test cases. "
            "If a candidate believes there is a technical error in grading, the recruiter must review "
            "and contact HackerRank support on the candidate's behalf. "
            "Support cannot instruct companies to advance candidates or change hiring decisions. "
            "Candidates cannot directly appeal scores through HackerRank support."
        ),
        "keywords": ["score", "score dispute", "grading", "unfair", "wrong score", "review answers",
                     "increase score", "next round", "rejected"],
    },
    {
        "id": "hr-011",
        "domain": "HackerRank",
        "product_area": "interviews",
        "title": "Mock Interviews – Refund Policy",
        "content": (
            "HackerRank SkillUp mock interviews are a paid service. "
            "If a mock interview stopped mid-session due to a technical issue, contact support "
            "with your session details. "
            "Refund eligibility depends on the circumstances and is evaluated case-by-case. "
            "Billing disputes and refund requests must be escalated to the billing or finance team. "
            "Candidates should provide the session ID, time, and description of the issue."
        ),
        "keywords": ["mock interview", "refund", "stopped", "billing", "payment", "skillup",
                     "interview refund"],
    },
    {
        "id": "hr-012",
        "domain": "HackerRank",
        "product_area": "screen",
        "title": "Payment / Order Issue (Subscriptions)",
        "content": (
            "For billing and payment issues related to HackerRank subscriptions, contact the billing team. "
            "Provide your order ID (e.g., cs_live_...) or invoice number. "
            "HackerRank support agents cannot directly process refunds — handled by the finance/billing team. "
            "Submit a billing support request via: "
            "https://portal.usepylon.com/hackerrank-support/forms/customer-request-form"
        ),
        "keywords": ["payment", "order", "order ID", "billing", "invoice", "charge",
                     "subscription payment", "cs_live"],
    },
    {
        "id": "hr-013",
        "domain": "HackerRank",
        "product_area": "general",
        "title": "Security / InfoSec Process",
        "content": (
            "HackerRank maintains security documentation including SOC 2 Type II reports and compliance materials. "
            "For enterprise security reviews (InfoSec questionnaires, vendor security forms, pen-test reports): "
            "contact your HackerRank account manager or submit via the customer request form. "
            "Security portal: https://security.hackerrank.com/ "
            "Support agents cannot fill in third-party InfoSec forms — handled by the security team."
        ),
        "keywords": ["infosec", "security", "questionnaire", "SOC2", "compliance", "vendor assessment",
                     "security form", "penetration test", "security review"],
    },
    {
        "id": "hr-014",
        "domain": "HackerRank",
        "product_area": "community",
        "title": "Practice / Apply Tab Not Visible",
        "content": (
            "If you cannot see the Apply tab or Practice section: "
            "1. Ensure you are logged into the correct HackerRank account. "
            "2. Verify the feature is available in your region. "
            "3. Update your browser and ensure cookies are enabled. "
            "4. Clear cache and cookies, then reload. "
            "The Apply tab connects job seekers to companies recruiting on HackerRank. "
            "If the issue persists, contact support with your browser and OS details."
        ),
        "keywords": ["apply tab", "practice", "job", "apply", "not visible", "missing tab",
                     "jobs", "submissions not working"],
    },
    {
        "id": "hr-015",
        "domain": "HackerRank",
        "product_area": "screen",
        "title": "Submissions Not Working Across Challenges",
        "content": (
            "If submissions are failing across multiple challenges, this may indicate a platform-wide issue. "
            "Troubleshooting steps: "
            "1. Check for current HackerRank maintenance windows. "
            "2. Try a different browser (Chrome recommended). "
            "3. Disable browser extensions that may interfere. "
            "4. Clear cache and cookies. "
            "If the issue persists across multiple users, it may be a platform bug — escalate to support "
            "with browser details, challenge name, language, and error message."
        ),
        "keywords": ["submission", "not working", "code submission", "platform issue", "challenge",
                     "error", "failing", "all challenges"],
    },
    {
        "id": "hr-016",
        "domain": "HackerRank",
        "product_area": "interviews",
        "title": "Zoom Connectivity / Compatible Check Blocker",
        "content": (
            "If Zoom connectivity fails during the HackerRank compatibility check: "
            "1. Ensure Zoom is installed and updated to the latest version. "
            "2. Allow camera and microphone permissions for the browser and Zoom. "
            "3. Disable VPN or firewall that may block Zoom. "
            "4. Allowlist Zoom domains as per HackerRank's safelist guide. "
            "5. Test Zoom independently at zoom.us/test. "
            "If all other criteria pass but Zoom still fails, contact support with system specs, "
            "browser version, and error details. The support team may arrange an alternate interview format."
        ),
        "keywords": ["zoom", "compatible check", "compatibility", "blocker", "interview", "camera",
                     "microphone", "connectivity", "VPN", "firewall"],
    },
    {
        "id": "hr-017",
        "domain": "HackerRank",
        "product_area": "screen",
        "title": "Rescheduling a HackerRank Assessment (Candidate Request)",
        "content": (
            "Candidates cannot directly reschedule HackerRank assessments through HackerRank support. "
            "The assessment schedule is controlled by the recruiting company (employer). "
            "To request a reschedule: contact the recruiter or HR team that sent you the invitation. "
            "HackerRank support can inform recruiters about the request but cannot override the company's "
            "hiring process. If the assessment link has expired, the recruiter must re-invite the candidate."
        ),
        "keywords": ["reschedule", "rescheduling", "assessment", "unable to attend", "alternative date",
                     "postpone", "candidate reschedule"],
    },
    {
        "id": "hr-018",
        "domain": "HackerRank",
        "product_area": "interviews",
        "title": "Interview Inactivity Timeout / Lobby Settings",
        "content": (
            "HackerRank Interviews has inactivity detection for both interviewers and candidates. "
            "If a user is inactive for a set period, they may be moved to a lobby or disconnected. "
            "Interviewers primarily watching a screen share may appear inactive. "
            "To extend inactivity times: contact HackerRank support — this is configurable at account level. "
            "Recommendation: interviewers should periodically interact with the HackerRank interface "
            "to avoid timeout."
        ),
        "keywords": ["inactivity", "timeout", "lobby", "disconnected", "screen share", "interviewer",
                     "candidate", "kicked out", "inactive"],
    },
    {
        "id": "hr-019",
        "domain": "HackerRank",
        "product_area": "settings",
        "title": "Removing a User / Interviewer from the Platform",
        "content": (
            "To remove an interviewer or user from HackerRank for Work: "
            "1. Go to Settings → Members. "
            "2. Find the user in the member list. "
            "3. Click the three-dot menu (⋮) next to their name. "
            "4. Select 'Remove member' or 'Deactivate'. "
            "If the option is not visible, you may not have admin or owner permissions. "
            "Contact your account admin to perform this action. "
            "Removed users lose access to the platform immediately."
        ),
        "keywords": ["remove user", "remove interviewer", "deactivate", "member", "three dots",
                     "settings", "employee leaving", "offboarding"],
    },
    {
        "id": "hr-020",
        "domain": "HackerRank",
        "product_area": "settings",
        "title": "Pausing or Cancelling HackerRank Subscription",
        "content": (
            "HackerRank subscriptions cannot be paused directly through the platform. "
            "To pause hiring: contact your HackerRank account manager or submit a request via the "
            "customer support form. "
            "Cancellation options depend on your contract type. "
            "For contract-based plans, early cancellation may have terms defined in your agreement. "
            "Submit requests at: https://portal.usepylon.com/hackerrank-support/forms/customer-request-form"
        ),
        "keywords": ["pause subscription", "cancel subscription", "stop hiring", "pause plan",
                     "subscription", "billing", "pause our subscription"],
    },
    {
        "id": "hr-021",
        "domain": "HackerRank",
        "product_area": "community",
        "title": "Resume Builder Feature",
        "content": (
            "HackerRank offers a Resume Builder feature for candidates to create and download resumes. "
            "If Resume Builder is down or inaccessible: "
            "1. Check for any active maintenance windows. "
            "2. Try a different browser or clear cache. "
            "3. Log out and log back in. "
            "If the issue persists, contact HackerRank support with your account email and browser details."
        ),
        "keywords": ["resume builder", "resume", "cv", "resume down", "resume not working",
                     "create resume"],
    },
    {
        "id": "hr-022",
        "domain": "HackerRank",
        "product_area": "screen",
        "title": "Certificate Name Update",
        "content": (
            "If your name is incorrect on your HackerRank certificate, contact HackerRank support. "
            "Provide: your account email, the assessment/test name, and the correct name. "
            "Certificate updates require identity verification — you may be asked for a government-issued ID. "
            "Processing time: typically 3–5 business days."
        ),
        "keywords": ["certificate", "name update", "wrong name", "incorrect name",
                     "certificate name", "update certificate"],
    },

    # ──────────────────────────────────────────────────────
    # CLAUDE
    # ──────────────────────────────────────────────────────
    {
        "id": "cl-001",
        "domain": "Claude",
        "product_area": "team_enterprise",
        "title": "Roles and Permissions in Team/Enterprise Plans",
        "content": (
            "Claude Team and Enterprise plans support four standard roles: "
            "Primary Owner (one per org, all permissions, uses one license seat), "
            "Owner (can manage billing, members, integrations — cannot provision seats or manage SSO), "
            "Admin (can manage features, integrations, members — cannot modify billing or provision seats), "
            "User (basic chat and project access). "
            "Only Admins and above can invite or remove members and modify roles. "
            "Billing and seat provisioning: Owner/Primary Owner only. "
            "Enterprise plans support custom roles for group-level feature access control."
        ),
        "keywords": ["team", "enterprise", "roles", "permissions", "admin", "owner", "workspace",
                     "seat", "access", "member"],
    },
    {
        "id": "cl-002",
        "domain": "Claude",
        "product_area": "team_enterprise",
        "title": "Restoring Workspace Access (Team/Enterprise)",
        "content": (
            "Access to a Claude team workspace is managed by your organization's admins and owners. "
            "If your seat was removed by an IT admin: "
            "- Contact your organization's Claude admin or IT admin to have your seat restored. "
            "- Claude support cannot restore access on behalf of non-admin users. "
            "- Only workspace Owners and Admins can manage member seats. "
            "If you are an owner locked out, contact Claude support via the Help Center."
        ),
        "keywords": ["workspace access", "team access", "lost access", "seat removed",
                     "restore access", "IT admin", "team workspace", "organization"],
    },
    {
        "id": "cl-003",
        "domain": "Claude",
        "product_area": "account_management",
        "title": "How to Delete Your Claude Account",
        "content": (
            "To delete your Claude account: "
            "1. Log in to Claude. "
            "2. Click your initials or name in the lower left corner. "
            "3. Select Settings → Account. "
            "4. Click 'Delete account' and follow the prompts. "
            "For paid subscribers: cancel your subscription in Billing settings first and wait for the "
            "current period to end. "
            "Data deletion is permanent — export your data beforehand if needed. "
            "Some accounts may need to contact support directly."
        ),
        "keywords": ["delete account", "close account", "remove account", "account deletion",
                     "permanently delete"],
    },
    {
        "id": "cl-004",
        "domain": "Claude",
        "product_area": "privacy",
        "title": "Deleting or Renaming a Conversation",
        "content": (
            "To delete an individual conversation in Claude: "
            "1. Navigate to the conversation. "
            "2. Click the conversation name at the top. "
            "3. Select 'Delete'. "
            "This permanently removes the conversation. "
            "For future privacy, use incognito chats (no conversation history saved). "
            "Reference: https://support.claude.com/en/articles/8230524"
        ),
        "keywords": ["delete conversation", "delete chat", "rename conversation", "private",
                     "sensitive info", "conversation history", "incognito"],
    },
    {
        "id": "cl-005",
        "domain": "Claude",
        "product_area": "privacy",
        "title": "Anthropic Web Crawling – Blocking ClaudeBot",
        "content": (
            "Anthropic uses three bots: ClaudeBot (AI training), Claude-User (live user queries), "
            "Claude-SearchBot (search indexing). "
            "To block Anthropic crawlers, add to your robots.txt: "
            "User-agent: ClaudeBot\nDisallow: /\n"
            "Robots.txt modifications are the recommended approach — blocking by IP is unreliable. "
            "Anthropic respects do-not-crawl signals and anti-circumvention technologies. "
            "Contact for crawler issues: privacy@anthropic.com"
        ),
        "keywords": ["crawl", "crawling", "bot", "claudebot", "robots.txt", "block crawler",
                     "website data", "scraping", "training data"],
    },
    {
        "id": "cl-006",
        "domain": "Claude",
        "product_area": "safeguards",
        "title": "Model Safety Bug Bounty / Vulnerability Reporting",
        "content": (
            "Anthropic operates a Model Safety Bug Bounty Program via HackerOne. "
            "Targets: universal jailbreaks — techniques that bypass safety protections across prompts. "
            "Bounties: up to $35,000 per novel universal jailbreak. "
            "Apply via the Google Form application. "
            "Participants must sign NDAs; cannot publicly disclose findings. "
            "Public vulnerability reporting: https://support.claude.com/en/articles/11427875 "
            "General security issues: use Anthropic's responsible disclosure program."
        ),
        "keywords": ["security vulnerability", "bug bounty", "jailbreak", "vulnerability",
                     "security issue", "report vulnerability", "hackerone", "exploit"],
    },
    {
        "id": "cl-007",
        "domain": "Claude",
        "product_area": "billing",
        "title": "Requesting a Refund for Claude Paid Plan",
        "content": (
            "Anthropic's policy: all payments are non-refundable except where stated in Consumer Terms "
            "or required by law. "
            "To request a refund: "
            "1. Log into Claude. 2. Initials → Get help → Send us a message. "
            "3. Choose 'Claude Refund Request'. 4. Select refund reason. 5. Follow prompts. "
            "iOS payments: contact Apple Support directly. "
            "Android payments: support team verifies; inactive subscriptions → Google Support. "
            "Active payment disputes: refunds cannot be processed while bank disputes are active."
        ),
        "keywords": ["refund", "billing", "payment", "cancel", "charge", "money back",
                     "subscription refund"],
    },
    {
        "id": "cl-008",
        "domain": "Claude",
        "product_area": "billing",
        "title": "Paid Plan Billing FAQs",
        "content": (
            "Invoices: Settings → Billing → View. Also auto-emailed. "
            "Updating payment: Settings → Billing → Update next to payment method. "
            "Invoice edits: once paid, invoices cannot be modified or reissued. "
            "Billing date changes: no direct way; unsubscribe and resubscribe on preferred date. "
            "Payment methods: only credit or debit cards accepted for Pro/Max. "
            "Account showing as free: verify correct email login or check for failed payments."
        ),
        "keywords": ["billing", "invoice", "payment method", "billing date", "credit card",
                     "debit card", "subscription billing"],
    },
    {
        "id": "cl-009",
        "domain": "Claude",
        "product_area": "troubleshooting",
        "title": "Troubleshooting Claude Errors / Not Responding",
        "content": (
            "If Claude is not responding or all requests are failing: "
            "1. Check Anthropic status page for outages. "
            "2. Refresh the browser or restart the app. "
            "3. Log out and log back in. "
            "4. Try a different network or disable VPN. "
            "5. Clear browser cache and cookies. "
            "For persistent issues, contact Claude support via Settings → Get help. "
            "Common errors: overloaded (try again later), invalid API key (check API console), "
            "context length exceeded (start new chat)."
        ),
        "keywords": ["not responding", "failing", "error", "outage", "not working",
                     "requests failing", "claude down", "503", "overloaded"],
    },
    {
        "id": "cl-010",
        "domain": "Claude",
        "product_area": "amazon_bedrock",
        "title": "Claude on Amazon Bedrock – Support Contact",
        "content": (
            "For Claude accessed via Amazon Bedrock: "
            "Contact AWS Support for support inquiries, or reach your AWS account manager. "
            "Community help: AWS re:Post. "
            "Refunds: Amazon Bedrock usage is non-refundable. "
            "Customers with private offers or direct Anthropic contracts may contact their "
            "Anthropic relationship manager. "
            "Documentation: docs.aws.amazon.com/bedrock"
        ),
        "keywords": ["amazon bedrock", "AWS", "bedrock", "bedrock support", "API failing",
                     "bedrock error", "aws bedrock"],
    },
    {
        "id": "cl-011",
        "domain": "Claude",
        "product_area": "education",
        "title": "Claude for Education – LTI Setup for Universities",
        "content": (
            "Claude for Education is an institutional plan for universities. "
            "LTI (Learning Tools Interoperability) setup guide: "
            "'Set up the Claude LTI in Canvas by Instructure' — "
            "https://support.claude.com/en/articles/11725453 "
            "Key steps: SSO setup, JIT or SCIM provisioning, security and user access configuration. "
            "Primary Owners and Owners receive direct Anthropic support. "
            "For professors setting up LTI keys for students: your university must have an active "
            "Claude for Education institutional plan first."
        ),
        "keywords": ["LTI", "canvas", "education", "university", "professor", "students",
                     "learning tools", "LTI key", "institution", "academic"],
    },
    {
        "id": "cl-012",
        "domain": "Claude",
        "product_area": "privacy",
        "title": "Personal Data Use & Retention",
        "content": (
            "By default, conversations may be used to improve Claude's models unless you opt out. "
            "To opt out: Settings → Privacy → disable 'Improve Claude for everyone'. "
            "Data retention: per the Privacy Policy and Terms of Service. "
            "Enterprise and Team plans have configurable data retention controls. "
            "Full details: privacy.anthropic.com "
            "To access/export data: Settings → Account → Export data. "
            "To delete data: delete conversations individually or delete your account."
        ),
        "keywords": ["personal data", "data use", "data retention", "training data", "how long",
                     "privacy", "data policy", "opt out", "conversation data"],
    },
    {
        "id": "cl-013",
        "domain": "Claude",
        "product_area": "safeguards",
        "title": "Claude Usage Policy – Prohibited Uses",
        "content": (
            "Claude's usage policy prohibits: generating content for malicious purposes, code to delete "
            "or damage systems, harmful content, CSAM, facilitating illegal activities, bypassing safety. "
            "Requests to generate harmful code (e.g., delete all files) are rejected. "
            "Prompt injection and jailbreak attempts are flagged and blocked. "
            "Report policy violations: https://support.claude.com/en/articles/10684638"
        ),
        "keywords": ["prohibited", "usage policy", "malicious", "delete files", "harmful",
                     "jailbreak", "prompt injection", "misuse", "abuse"],
    },

    # ──────────────────────────────────────────────────────
    # VISA
    # ──────────────────────────────────────────────────────
    {
        "id": "vs-001",
        "domain": "Visa",
        "product_area": "credit_cards",
        "title": "How to Log In / Check Balance / Pay Bill",
        "content": (
            "To log in to your credit card account to pay your bill or check your balance, "
            "visit your card issuer's or bank's website directly. "
            "The contact information is typically on the back of your card. "
            "Visa does not directly manage individual cardholder accounts — your issuing bank does."
        ),
        "keywords": ["log in", "account", "pay bill", "check balance", "credit card account",
                     "issuer", "bank"],
    },
    {
        "id": "vs-002",
        "domain": "Visa",
        "product_area": "credit_cards",
        "title": "How to Dispute a Charge on Your Visa Card",
        "content": (
            "To dispute a charge on your Visa card: "
            "Contact your card issuer or bank using the phone number on the back of your card. "
            "Your issuer will require detailed information about the transaction before resolving the dispute. "
            "You can also initiate a dispute online through your bank's portal. "
            "Visa's dispute resolution rules require issuers to process disputes within specified timeframes. "
            "Keep records of any merchant communications as evidence."
        ),
        "keywords": ["dispute", "dispute charge", "chargeback", "wrong charge",
                     "transaction dispute", "billing dispute", "merchant dispute"],
    },
    {
        "id": "vs-003",
        "domain": "Visa",
        "product_area": "credit_cards",
        "title": "Why Was My Visa Card Declined?",
        "content": (
            "Your Visa card may be declined for various reasons. "
            "Your issuer or bank is best equipped to provide the specific decline reason. "
            "Common reasons: insufficient funds, card expired, card blocked for security, "
            "unusual spending pattern flagged. "
            "Contact your financial institution using the number on your card to resolve the issue."
        ),
        "keywords": ["card declined", "declined", "rejected", "card not working",
                     "payment declined"],
    },
    {
        "id": "vs-004",
        "domain": "Visa",
        "product_area": "security",
        "title": "Lost or Stolen Visa Card",
        "content": (
            "If your Visa card is lost or stolen: "
            "Contact your card issuer immediately using the number on your card. "
            "India: Call Visa India at 000-800-100-1219. "
            "Global 24/7: Visa Global Customer Assistance Service at +1 303 967 1090. "
            "Reporting blocks your card (typically ~30 minutes) and can arrange emergency cash "
            "and replacement. "
            "Also notify local police if stolen."
        ),
        "keywords": ["lost card", "stolen card", "missing card", "block card", "card stolen",
                     "lost visa", "report stolen", "emergency card"],
    },
    {
        "id": "vs-005",
        "domain": "Visa",
        "product_area": "general_support",
        "title": "Find a Visa ATM / Urgent Cash",
        "content": (
            "Use Visa's ATM locator to find an ATM and get currency at over 2 million ATMs worldwide. "
            "Visit visa.co.in or the Visa global website for the ATM locator tool. "
            "Most Visa cards can be used at any ATM displaying the Visa or PLUS logo. "
            "For cash advances on a credit card, check with your issuer about applicable fees. "
            "For emergency cash assistance while traveling, call: +1 303 967 1090 (24/7)."
        ),
        "keywords": ["ATM", "find ATM", "cash", "currency", "ATM locator", "cash advance",
                     "urgent cash", "need money", "emergency cash"],
    },
    {
        "id": "vs-006",
        "domain": "Visa",
        "product_area": "security",
        "title": "Scam / Fraud – Someone Claiming to Be Visa",
        "content": (
            "Visa does NOT call or email cardholders to request personal information. "
            "If you are contacted by someone claiming to be from Visa and asking for personal details, "
            "it is a scam. "
            "Do not provide any information to unsolicited callers or emails. "
            "Report suspected Visa-related fraud to your bank and to local authorities."
        ),
        "keywords": ["scam", "fraud", "claiming to be visa", "phishing", "fake visa",
                     "impersonation", "unsolicited call", "suspicious call"],
    },
    {
        "id": "vs-007",
        "domain": "Visa",
        "product_area": "security",
        "title": "Identity Theft – What to Do",
        "content": (
            "If your identity has been stolen: "
            "1. Visit the Lost or Stolen card page on visa.co.in to learn about canceling your card "
            "or obtaining emergency replacement. "
            "2. Contact your card issuer immediately to freeze all accounts. "
            "3. File a police report. "
            "4. Contact credit bureaus (CIBIL in India) to place a fraud alert on your credit file. "
            "5. Monitor your accounts closely for unauthorized transactions. "
            "This is a high-urgency situation — escalate immediately."
        ),
        "keywords": ["identity theft", "identity stolen", "fraud", "stolen identity",
                     "unauthorized", "credit bureau", "freeze account"],
    },
    {
        "id": "vs-008",
        "domain": "Visa",
        "product_area": "travel_support",
        "title": "Travel Abroad with Your Visa Card",
        "content": (
            "Before travelling abroad: notify your issuing bank of travel dates and destinations. "
            "Know your card's international transaction fees. "
            "Emergency number: +1 800 847 2911 (USA) or global numbers on visa.co.in. "
            "For a damaged card during travel: emergency replacement delivered within 1–3 days. "
            "Call +1 800 847 2911 or use global numbers from the visa.co.in dropdown."
        ),
        "keywords": ["travel", "abroad", "international", "overseas", "travel card",
                     "foreign travel", "emergency abroad"],
    },
    {
        "id": "vs-009",
        "domain": "Visa",
        "product_area": "travel_support",
        "title": "Lost or Stolen Visa Traveller's Cheques",
        "content": (
            "If your Visa Traveller's Cheques are stolen: "
            "Call the cheque issuer (e.g., Citicorp) immediately. "
            "Citicorp: Freephone 1-800-645-6556 or collect 1-813-623-1709, Mon–Fri 6:30am–2:30pm EST. "
            "Automated verification available 24/7 in English/Spanish. "
            "Have ready: cheque serial numbers, purchase location/date, how/when stolen, issuer name. "
            "Refunds can typically be arranged within 24 hours, subject to T&Cs. "
            "Also notify local police. "
            "If unable to reach issuer, use Visa's traveller's-cheque contact form on visa.co.in."
        ),
        "keywords": ["traveller's cheque", "travelers cheque", "stolen cheque", "cheque refund",
                     "citicorp", "travel cheque"],
    },
    {
        "id": "vs-010",
        "domain": "Visa",
        "product_area": "security",
        "title": "3-D Secure (Verified by Visa)",
        "content": (
            "3-D Secure provides an additional layer of security for e-commerce transactions. "
            "As a consumer, there is nothing you need to register for — your issuer handles "
            "authentication automatically. "
            "If 3-D Secure is not working: contact your issuer or bank using the number on your card. "
            "3-D Secure is triggered at checkout on participating merchant sites."
        ),
        "keywords": ["3d secure", "verified by visa", "authentication", "online payment",
                     "ecommerce", "OTP", "payment verification"],
    },
    {
        "id": "vs-011",
        "domain": "Visa",
        "product_area": "merchants",
        "title": "Merchant Minimum Transaction Limits",
        "content": (
            "Generally, merchants cannot set a minimum or maximum transaction amount for Visa purchases. "
            "Exception: In the USA and US territories (including US Virgin Islands), "
            "a merchant may require a minimum transaction amount of US$10 for credit card purchases only. "
            "This does not apply to debit cards. "
            "If a merchant violates Visa's rules, you can file a complaint on the Visa website."
        ),
        "keywords": ["minimum spend", "minimum transaction", "merchant limit",
                     "transaction minimum", "10 dollar minimum", "US Virgin Islands",
                     "merchant rules"],
    },
    {
        "id": "vs-012",
        "domain": "Visa",
        "product_area": "merchants",
        "title": "Concerns About a Merchant (Complaint)",
        "content": (
            "If you have concerns about a merchant where you used your Visa card: "
            "File a complaint using the form provided on the Visa website (visa.co.in or visa.com). "
            "For disputes about a specific transaction (wrong product, not received), contact your "
            "issuing bank to dispute the charge. "
            "Visa can investigate merchant rule violations but cannot directly mandate refunds — "
            "your bank's dispute process covers individual transaction issues."
        ),
        "keywords": ["merchant concern", "complaint", "wrong product", "merchant dispute",
                     "seller", "ban merchant", "merchant violation"],
    },
    {
        "id": "vs-013",
        "domain": "Visa",
        "product_area": "credit_cards",
        "title": "Emergency Visa Card Replacement",
        "content": (
            "Emergency card replacement is available for lost, stolen, or damaged Visa cards. "
            "Emergency cards typically delivered within 1–3 days. "
            "Call USA support: +1 800 847 2911 or global emergency numbers from visa.co.in. "
            "Global 24/7 assistance: +1 303 967 1090. "
            "Your issuing bank can also arrange emergency cash while you wait for the replacement."
        ),
        "keywords": ["emergency card", "replacement card", "damaged card", "card replacement",
                     "emergency replacement", "travel emergency"],
    },
    {
        "id": "vs-014",
        "domain": "Visa",
        "product_area": "security",
        "title": "Visa Card Blocked – Fraud Prevention",
        "content": (
            "If your Visa card has been blocked, it may be due to: "
            "1. Suspected fraudulent activity detected by your issuer. "
            "2. Unusual transactions in an unfamiliar location (e.g., abroad). "
            "3. Multiple failed PIN attempts. "
            "To unblock: contact your issuing bank using the number on your card. "
            "Visa's Global Customer Assistance: +1 303 967 1090 (24/7). "
            "India: 000-800-100-1219. "
            "Internal fraud detection rules and processes are confidential and cannot be disclosed."
        ),
        "keywords": ["card blocked", "blocked card", "frozen card", "card not working",
                     "fraud block", "unblock card", "card declined abroad"],
    },
]


def get_corpus_by_domain(domain: str) -> list[dict]:
    return [d for d in CORPUS if d["domain"].lower() == domain.lower()]


def get_all_domains() -> list[str]:
    return ["HackerRank", "Claude", "Visa"]
