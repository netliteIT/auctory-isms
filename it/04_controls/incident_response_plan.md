# Piano di risposta agli incidenti

> Versione: 2026-02-26  
> Proprietario: Andrea Gagliardi

## Definizioni
- **Evento**: occorrenza osservabile.
- **Incidente**: evento con impatto su sicurezza (CIA) o potenziale violazione.

## Fasi
1. Preparazione (runbook, contatti, accessi, tooling)
2. Identificazione e triage (entro 24h)
3. Containment (limitare impatto)
4. Eradicazione e ripristino
5. Lessons learned (post-mortem) e aggiornamento rischio/controlli

## Registrazione
- Ogni incidente viene registrato in `incident_register.yaml`.
- Evidenze raccolte in `evidence/` (redatte se necessario).
