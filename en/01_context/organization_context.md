# Organization context

> Version: 2026-02-26  
> Owner: Andrea Gagliardi

## Operating model
- Distributed team (remote-first), 3 people with infrastructure access.
- Main tooling: GitHub, Hetzner Cloud, overlay network (e.g., Tailscale) for administrative access.
- Architecture: customer-dedicated VMs (strong segregation).

## Information types
- Industrial operational data (telemetry/production).
- System and application logs.
- Infrastructure configuration data (IaC, secrets handled per policy).

## Security objectives
Protect confidentiality, integrity and availability of:
- customer systems and data within the Auctory perimeter,
- source code and CI/CD pipelines,
- credentials and cryptographic keys,
- ISMS documentation and records.
