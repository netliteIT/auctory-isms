# Politica backup e restore

> Versione: 2026-02-26  
> Proprietario: Andrea Gagliardi

## Scope
Backup delle VM cloud per-cliente (Hetzner) e backup dei dati applicativi dove applicabile.

## Policy
- Snapshot/backup VM secondo policy definita (retention minima da stabilire per classe cliente).
- Restore test: almeno annuale (o più frequente per clienti enterprise), con evidenza in `backup_test_register.yaml`.

## Requisiti
- Definire RPO/RTO per classi di servizio.
- Documentare procedura di restore (link a runbook/issue) e outcome.

## Note
Il fatto che la capability di backup sia offerta dal provider non esime Auctory da:
- definire e verificare la policy,
- testare il ripristino,
- mantenere evidenze.
