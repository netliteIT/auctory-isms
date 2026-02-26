# Logging and monitoring policy

> Version: 2026-02-26  
> Owner: Andrea Gagliardi

## Logging
- Centralized system and application logging per customer setup via syslog.
- Log retention and access defined per customer tier and legal/contractual requirements.
- Log protection: restricted access, integrity (immutability where feasible).

## Monitoring
- Each customer setup includes a Prometheus-based metrics server.
- Alerting for critical events (e.g., storage saturation, service down, anomalies).

## Use in incident response
- Logs and metrics support detection, triage, containment and post-mortem.
