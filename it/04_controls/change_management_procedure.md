# Procedura di Change Management

> Versione: 2026-02-26  
> Proprietario: Andrea Gagliardi

## Scopo
Garantire che i cambi a produzione siano autorizzati, testati e tracciabili.

## Regole
- Ogni change a produzione richiede:
  - ticket/issue o change record
  - PR con review
  - evidenza test (staging) ove applicabile
- Deploy: preferibilmente automatizzato (CI/CD) con log dei rilasci.
- Rollback: definire strategia per componente (documentare nei runbook di servizio).
