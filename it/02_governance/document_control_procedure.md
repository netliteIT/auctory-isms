# Procedura di controllo documenti (ISMS-as-Code)

> Versione: 2026-02-26  
> Proprietario: Andrea Gagliardi

## Scopo
Garantire che la documentazione ISMS sia controllata, aggiornata, approvata e tracciabile.

## Regole
- Tutti i documenti ISMS risiedono in questo repository Git.
- Le modifiche avvengono tramite **Pull Request** con review obbligatoria.
- Branch protection raccomandata:
  - PR required
  - almeno 1 reviewer
  - status checks (CI) se applicabili
- Ogni documento riporta una data/versione nella prima pagina.
- Dopo il Management Review annuale viene creato un **tag di release** (es. `ISMS-2026-v1.0`).

## Conservazione
- La history Git costituisce il registro di versioning.
- Backup del repository: secondo policy del provider (GitHub) + export periodico (opzionale).
