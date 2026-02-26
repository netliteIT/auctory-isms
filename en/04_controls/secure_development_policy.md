# Secure development policy

> Version: 2026-02-26  
> Owner: Andrea Gagliardi

## Workflow
- All changes via Pull Request.
- Mandatory code review.
- Branch protection (main/prod): merge only with review and checks.

## Vulnerability management
- Dependency scanning (e.g., Dependabot) enabled.
- High/Critical vulnerabilities: handled within internal SLA and tracked via issues.

## Environment separation
- Dev/Staging/Prod separated (control 8.31).
- Production data not used in dev/test unless anonymized or explicitly authorized.

## Source code access
- Role-based access; private repositories as needed.
- GitHub audit trail enabled.
