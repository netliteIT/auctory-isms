# Access control policy

> Version: 2026-02-26  
> Owner: Andrea Gagliardi

## Principles
- Least privilege, need-to-know, separation of duties where applicable.
- Mandatory MFA for all critical accounts (GitHub, Hetzner, overlay network).
- Preference for hardware security keys (Yubikey/passkeys).

## Privileged access
- Root/admin access only when operationally required.
- All privileged access must be logged and recorded in `privileged_access_register.yaml`.

## Identity management (high level)
- Onboarding: account creation, role assignment, MFA enablement.
- Offboarding: access revocation, key/secret rotation, session termination.

## Infrastructure access
- Administrative access to VMs only through overlay network + MFA.
- SSH key auth; disable SSH passwords where possible.
