# Cryptography policy

> Version: 2026-02-26  
> Owner: Andrea Gagliardi

## Objective
Protect data in transit and, where applicable, at rest.

## Guidelines
- TLS for application/API traffic.
- SSH key-based access.
- Full disk encryption on user endpoints.
- Key management:
  - protect private keys (hardware keys where feasible)
  - rotate keys after incidents/offboarding

## Secrets
- Secrets/tokens MUST NOT be committed to the repo.
- Use secret managers / CI/CD variables / vault according to product architecture.
