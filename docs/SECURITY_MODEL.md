# Security Model

Target: private invite-only use for approximately 10–12 users.

Requirements:
- private GitHub repository
- no secrets in Git
- `.env` ignored
- secure production secret store
- PKCE/RS256 human authentication
- server-side roles/ownership
- OWNER / MEMBER initially
- per-user portfolio isolation
- HTTPS
- explicit CORS
- rate limiting before Internet exposure
- no broker order authority
- sanitized logs
- encrypted backups before production use
