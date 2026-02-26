# Incident response plan

> Version: 2026-02-26  
> Owner: Andrea Gagliardi

## Definitions
- **Event**: observable occurrence.
- **Incident**: event impacting (or potentially impacting) security (CIA) or involving a breach.

## Phases
1. Preparation (runbooks, contacts, access, tooling)
2. Identification & triage (within 24h)
3. Containment (limit impact)
4. Eradication & recovery
5. Lessons learned (post-mortem) and updates to risk/controls

## Recording
- Every incident is recorded in `incident_register.yaml`.
- Evidence stored under `evidence/` (redacted when needed).
