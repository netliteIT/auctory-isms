# Politica Secure Development

> Versione: 2026-02-26  
> Proprietario: Andrea Gagliardi

## Workflow
- Tutte le modifiche passano da Pull Request.
- Code review obbligatoria.
- Branch protection (main/prod): merge solo con review e checks.

## Vulnerability management
- Dependency scanning (es. Dependabot) abilitato.
- Vulnerabilità High/Critical: gestione entro SLA interno e registrazione issue.

## Separazione ambienti
- Dev/Staging/Prod separati (controllo 8.31).
- Dati produzione non usati in dev/test salvo anonimizzazione o autorizzazione.

## Accesso al codice sorgente
- Accesso per ruoli; repository privati se necessario.
- Log e audit trail GitHub.
