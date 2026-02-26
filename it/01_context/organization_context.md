# Contesto dell’organizzazione

> Versione: 2026-02-26  
> Proprietario: Andrea Gagliardi

## Modello operativo
- Team distribuito (remote-first), 3 persone con accesso infrastrutturale.
- Tooling principale: GitHub, Hetzner Cloud, overlay network (es. Tailscale) per accesso amministrativo.
- Architettura: setup per-cliente su VM dedicate (segregazione forte).

## Tipologia informazioni trattate
- Dati industriali operativi (telemetrie/produzione).
- Log applicativi e sistemistici.
- Dati di configurazione infrastrutturale (IaC, secrets gestiti secondo policy).

## Obiettivi di sicurezza
Proteggere riservatezza, integrità e disponibilità di:
- sistemi e dati dei clienti ospitati nel perimetro Auctory,
- codice sorgente e pipeline CI/CD,
- credenziali e chiavi crittografiche,
- documentazione e registrazioni ISMS.
