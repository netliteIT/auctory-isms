# Campo di applicazione (Scope) ISMS

> Versione: 2026-02-26  
> Proprietario: Andrea Gagliardi

## Organizzazione
Auctory (startup software).

## Campo di applicazione
L’ISMS copre la **progettazione, sviluppo, rilascio e gestione operativa** delle soluzioni **SaaS Auctory** per acquisizione ed elaborazione dati industriali, ospitate su **VM cloud dedicate per singolo cliente** presso Hetzner.

## Componenti inclusi
- Repositori e pipeline di sviluppo su GitHub (code, IaC, CI/CD, documentazione operativa).
- Ambienti separati: **dev / staging / prod**.
- Infrastruttura cloud per-cliente (VM dedicate, networking, firewalling, storage).
- Meccanismi di accesso remoto e amministrazione (SDN/overlay network) per il team Auctory.
- Logging centralizzato sistemistico e applicativo basato su syslog.
- Metriche e monitoraggio per setup cliente basati su Prometheus.

## Componenti esclusi
- Infrastrutture fisiche (Auctory non gestisce datacenter).
- Sistemi on-premise del cliente, salvo quanto espressamente contrattualizzato.
- Gateway hardware: esclusi dallo scope; la gestione fleet è delegata a Balena Cloud (fornitore certificato ISO 27001).

## Confini logici
- Segregazione primaria tramite **VM dedicate per cliente**.
- Accessi amministrativi consentiti solo tramite overlay network autenticata e MFA con hardware keys.

## Assunzioni e dipendenze
- Hetzner fornisce servizi di snapshot/backup per le VM; Auctory definisce policy, retention e test di ripristino.
