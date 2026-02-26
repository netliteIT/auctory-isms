# Backup and restore policy

> Version: 2026-02-26  
> Owner: Andrea Gagliardi

## Scope
Backups of customer-dedicated cloud VMs (Hetzner) and application data where applicable.

## Policy
- VM snapshots/backups per defined policy (minimum retention to be set per customer tier).
- Restore test: at least annually (or more frequently for enterprise customers), recorded in `backup_test_register.yaml`.

## Requirements
- Define RPO/RTO per service tier.
- Document restore procedure (link to runbook/issue) and outcome.

## Note
Provider backup capability does not remove Auctory responsibility to:
- define and verify the policy,
- test restores,
- keep evidence.
