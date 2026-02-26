# Politica crittografica

> Versione: 2026-02-26  
> Proprietario: Andrea Gagliardi

## Obiettivo
Proteggere dati in transito e, dove applicabile, a riposo.

## Linee guida
- TLS per traffico applicativo e API.
- SSH con chiavi.
- Cifratura disco su endpoint utente (full disk encryption).
- Gestione chiavi:
  - chiavi private protette (hardware keys dove possibile)
  - rotazione in caso di incidente/offboarding

## Segreti
- Segreti e token NON devono essere committati nel repo.
- Usare secret manager / variabili CI/CD / vault secondo architettura del prodotto.
