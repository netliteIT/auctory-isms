# Politica di controllo accessi

> Versione: 2026-02-26  
> Proprietario: Andrea Gagliardi

## Principi
- Least privilege, need-to-know, separation of duties dove applicabile.
- MFA obbligatoria per tutti gli account critici (GitHub, Hetzner, overlay network).
- Preferenza per hardware security keys (Yubikey/passkey).

## Accessi privilegiati
- Accessi root/admin solo per necessità operativa.
- Tutti gli accessi privilegiati devono essere tracciati (log) e registrati nel `privileged_access_register.yaml`.

## Gestione identità (high level)
- Onboarding: creazione account, assegnazione ruoli, abilitazione MFA.
- Offboarding: revoca accessi, rotazione chiavi/segreti, chiusura sessioni.

## Accesso infrastruttura
- Accesso amministrativo alle VM solo tramite overlay network e MFA.
- Accesso SSH con chiavi; password SSH disabilitate ove possibile.
