# Supplier security policy

> Version: 2026-02-26  
> Owner: Andrea Gagliardi

## Critical suppliers (typical)
- Hetzner (cloud)
- GitHub (code + audit trail)
- Overlay network provider (e.g., Tailscale)
- Balena Cloud (out-of-scope for gateways, but service dependency)

## Requirements
- Supplier register: `supplier_register.yaml`
- Initial risk assessment and annual review
- Monitor contractual changes / known incidents
- Minimum clauses: confidentiality, availability, incident notification (where feasible)
