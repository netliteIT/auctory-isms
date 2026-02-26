# ISMS Scope

> Version: 2026-02-26  
> Owner: Andrea Gagliardi

## Organization
Auctory (software startup).

## Scope
The ISMS covers the **design, development, release and operational management** of **Auctory SaaS** solutions for industrial data acquisition and processing, hosted on **customer-dedicated cloud VMs** at Hetzner.

## In scope
- GitHub repositories and development pipelines (code, IaC, CI/CD, operational documentation).
- Segregated environments: **dev / staging / prod**.
- Customer-dedicated cloud infrastructure (VMs, networking, firewalling, storage).
- Remote administration via authenticated overlay/SDN network.
- Centralized system and application logging via syslog.
- Customer setup metrics/monitoring via Prometheus.

## Out of scope
- Physical infrastructure (Auctory does not operate a datacenter).
- Customer on-prem systems unless explicitly contracted.
- Hardware gateways: out of scope; fleet management is delegated to Balena Cloud (ISO 27001 certified provider).

## Logical boundaries
- Primary segregation through **one dedicated VM set per customer**.
- Administrative access only via authenticated overlay network + MFA with hardware security keys.

## Dependencies
- Hetzner provides VM snapshot/backup capabilities; Auctory defines policy, retention and restore testing.
