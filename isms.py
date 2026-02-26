import os, textwrap, zipfile, datetime, pathlib, re, json, hashlib

base = pathlib.Path(".")

def write(rel, content):
    path = base / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")

today = datetime.date(2026,2,26).isoformat()

# Common README
write("README.md", textwrap.dedent(f"""\
# Auctory ISMS (ISO/IEC 27001:2022)

This repository contains the Information Security Management System (ISMS) documentation for **Auctory**,
maintained as **ISMS-as-Code** (version-controlled, pull-request based).

- Standard: ISO/IEC 27001:2022
- Owner / ISMS Manager: Andrea Gagliardi
- Last generated: {today}

## How to use this repo
- Changes MUST be made via Pull Request (PR) and reviewed.
- Tag a release after each annual Management Review (e.g. `ISMS-2026-v1.0`).
- Evidence is stored under `evidence/` (or referenced with immutable links).

## Languages
- Italian: `it/`
- English: `en/`

## Quick start
1. Read `*/01_context/scope.md`
2. Read `*/02_governance/information_security_policy.md`
3. Review risk management in `03_risk_management/`
4. Review Annex A in `06_annex_a/statement_of_applicability.yaml`
"""))

write("VERSION", "0.1.0\n")

write("evidence/README.md", textwrap.dedent("""\
# Evidence

Place audit evidence here or reference it via immutable links.

Recommended structure:
- `restore-tests/`
- `screenshots/`
- `exports/`
- `tickets/`
- `logs/`

Rules:
- Avoid secrets in evidence.
- Prefer redaction over deletion.
- Evidence must be time-bound (date), attributable (who/where), and immutable (checksum if possible).
"""))

# Language directories
langs = ["it","en"]

# Control list (from Advisera, ids and names) - keep as authoritative mapping
controls = []
# 5.1-5.37
org_names = [
"Policies for information security",
"Information security roles and responsibilities",
"Segregation of duties",
"Management responsibilities",
"Contact with authorities",
"Contact with special interest groups",
"Threat intelligence",
"Information security in project management",
"Inventory of information and other associated assets",
"Acceptable use of information and other associated assets",
"Return of assets",
"Classification of information",
"Labelling of information",
"Information transfer",
"Access control",
"Identity management",
"Authentication information",
"Access rights",
"Information security in supplier relationships",
"Addressing information security within supplier agreements",
"Managing information security in the ICT supply chain",
"Monitoring, review and change management of supplier service",
"Information security for use of cloud services",
"Information security incident management planning and preparation",
"Assessment and decision on information security events",
"Response to information security incidents",
"Learning from information security incidents",
"Collection of evidence",
"Information security during disruption",
"ICT readiness for business continuity",
"Legal, statutory, regulatory and contractual requirements",
"Intellectual property rights",
"Protection of records",
"Privacy and protection of PII",
"Independent review of information security",
"Compliance with policies, rules and standards for information security",
"Documented operating procedures",
]
for i,name in enumerate(org_names, start=1):
    controls.append((f"5.{i}", name))

people_names = [
"Screening",
"Terms and conditions of employment",
"Information security awareness, education and training",
"Disciplinary process",
"Responsibilities after termination or change of employment",
"Confidentiality or non-disclosure agreements",
"Remote working",
"Information security event reporting",
]
for i,name in enumerate(people_names, start=1):
    controls.append((f"6.{i}", name))

physical_names = [
"Physical security perimeters",
"Physical entry",
"Securing offices, rooms and facilities",
"Physical security monitoring",
"Protecting against physical and environmental threats",
"Working in secure areas",
"Clear desk and clear screen",
"Equipment siting and protection",
"Security of assets off-premises",
"Storage media",
"Supporting utilities",
"Cabling security",
"Equipment maintenance",
"Secure disposal or re-use of equipment",
]
for i,name in enumerate(physical_names, start=1):
    controls.append((f"7.{i}", name))

tech_names = [
"User endpoint devices",
"Privileged access rights",
"Information access restriction",
"Access to source code",
"Secure authentication",
"Capacity management",
"Protection against malware",
"Management of technical vulnerabilities",
"Configuration management",
"Information deletion",
"Data masking",
"Data leakage prevention",
"Information backup",
"Redundancy of information processing facilities",
"Logging",
"Monitoring activities",
"Clock synchronization",
"Use of privileged utility programs",
"Installation of software on operational systems",
"Networks security",
"Security of network services",
"Segregation of networks",
"Web filtering",
"Use of cryptography",
"Secure development life cycle",
"Application security requirements",
"Secure system architecture and engineering principles",
"Secure coding",
"Security testing in development and acceptance",
"Outsourced development",
"Separation of development, test and production environments",
"Change management",
"Test information",
"Protection of information systems during audit testing",
]
for i,name in enumerate(tech_names, start=1):
    controls.append((f"8.{i}", name))

assert len(controls)==93

# Minimal Italian translations (pragmatic, not literary)
it_map = {
"Policies for information security":"Politiche per la sicurezza delle informazioni",
"Information security roles and responsibilities":"Ruoli e responsabilità per la sicurezza delle informazioni",
"Segregation of duties":"Segregazione dei compiti",
"Management responsibilities":"Responsabilità della direzione",
"Contact with authorities":"Contatto con le autorità",
"Contact with special interest groups":"Contatto con gruppi di interesse",
"Threat intelligence":"Threat intelligence",
"Information security in project management":"Sicurezza delle informazioni nel project management",
"Inventory of information and other associated assets":"Inventario delle informazioni e degli asset associati",
"Acceptable use of information and other associated assets":"Uso accettabile delle informazioni e degli asset associati",
"Return of assets":"Restituzione degli asset",
"Classification of information":"Classificazione delle informazioni",
"Labelling of information":"Etichettatura delle informazioni",
"Information transfer":"Trasferimento delle informazioni",
"Access control":"Controllo degli accessi",
"Identity management":"Gestione delle identità",
"Authentication information":"Informazioni di autenticazione",
"Access rights":"Diritti di accesso",
"Information security in supplier relationships":"Sicurezza delle informazioni nei rapporti con i fornitori",
"Addressing information security within supplier agreements":"Sicurezza delle informazioni negli accordi con i fornitori",
"Managing information security in the ICT supply chain":"Gestione della sicurezza delle informazioni nella supply chain ICT",
"Monitoring, review and change management of supplier service":"Monitoraggio, riesame e gestione cambiamenti dei servizi del fornitore",
"Information security for use of cloud services":"Sicurezza delle informazioni per l’uso di servizi cloud",
"Information security incident management planning and preparation":"Pianificazione e preparazione per la gestione degli incidenti di sicurezza",
"Assessment and decision on information security events":"Valutazione e decisione sugli eventi di sicurezza",
"Response to information security incidents":"Risposta agli incidenti di sicurezza",
"Learning from information security incidents":"Apprendimento dagli incidenti di sicurezza",
"Collection of evidence":"Raccolta delle evidenze",
"Information security during disruption":"Sicurezza delle informazioni durante interruzioni",
"ICT readiness for business continuity":"Prontezza ICT per la continuità operativa",
"Legal, statutory, regulatory and contractual requirements":"Requisiti legali, statutari, normativi e contrattuali",
"Intellectual property rights":"Diritti di proprietà intellettuale",
"Protection of records":"Protezione delle registrazioni",
"Privacy and protection of PII":"Privacy e protezione dei dati personali (PII)",
"Independent review of information security":"Riesame indipendente della sicurezza delle informazioni",
"Compliance with policies, rules and standards for information security":"Conformità a politiche, regole e standard di sicurezza",
"Documented operating procedures":"Procedure operative documentate",
"Screening":"Selezione / verifica preliminare",
"Terms and conditions of employment":"Termini e condizioni di lavoro",
"Information security awareness, education and training":"Consapevolezza, formazione e addestramento",
"Disciplinary process":"Processo disciplinare",
"Responsibilities after termination or change of employment":"Responsabilità dopo cessazione o cambio rapporto",
"Confidentiality or non-disclosure agreements":"Accordi di riservatezza / NDA",
"Remote working":"Lavoro da remoto",
"Information security event reporting":"Segnalazione eventi di sicurezza",
"Physical security perimeters":"Perimetri di sicurezza fisica",
"Physical entry":"Accesso fisico",
"Securing offices, rooms and facilities":"Messa in sicurezza di uffici, locali e strutture",
"Physical security monitoring":"Monitoraggio della sicurezza fisica",
"Protecting against physical and environmental threats":"Protezione da minacce fisiche e ambientali",
"Working in secure areas":"Lavoro in aree sicure",
"Clear desk and clear screen":"Scrivania pulita e schermo pulito",
"Equipment siting and protection":"Posizionamento e protezione delle apparecchiature",
"Security of assets off-premises":"Sicurezza degli asset fuori sede",
"Storage media":"Supporti di memorizzazione",
"Supporting utilities":"Servizi di supporto",
"Cabling security":"Sicurezza dei cablaggi",
"Equipment maintenance":"Manutenzione delle apparecchiature",
"Secure disposal or re-use of equipment":"Smaltimento sicuro o riuso delle apparecchiature",
"User endpoint devices":"Dispositivi endpoint utente",
"Privileged access rights":"Diritti di accesso privilegiato",
"Information access restriction":"Restrizione dell’accesso alle informazioni",
"Access to source code":"Accesso al codice sorgente",
"Secure authentication":"Autenticazione sicura",
"Capacity management":"Gestione della capacità",
"Protection against malware":"Protezione contro malware",
"Management of technical vulnerabilities":"Gestione delle vulnerabilità tecniche",
"Configuration management":"Gestione della configurazione",
"Information deletion":"Cancellazione delle informazioni",
"Data masking":"Mascheramento dei dati",
"Data leakage prevention":"Prevenzione della perdita di dati",
"Information backup":"Backup delle informazioni",
"Redundancy of information processing facilities":"Ridondanza delle risorse di elaborazione",
"Logging":"Logging",
"Monitoring activities":"Monitoraggio delle attività",
"Clock synchronization":"Sincronizzazione dell’orologio",
"Use of privileged utility programs":"Uso di utility privilegiate",
"Installation of software on operational systems":"Installazione software su sistemi operativi",
"Networks security":"Sicurezza delle reti",
"Security of network services":"Sicurezza dei servizi di rete",
"Segregation of networks":"Segregazione delle reti",
"Web filtering":"Filtraggio web",
"Use of cryptography":"Uso della crittografia",
"Secure development life cycle":"Ciclo di vita di sviluppo sicuro (SDLC)",
"Application security requirements":"Requisiti di sicurezza applicativa",
"Secure system architecture and engineering principles":"Architettura e principi di ingegneria sicura",
"Secure coding":"Codifica sicura",
"Security testing in development and acceptance":"Test di sicurezza in sviluppo e accettazione",
"Outsourced development":"Sviluppo in outsourcing",
"Separation of development, test and production environments":"Separazione ambienti sviluppo, test e produzione",
"Change management":"Gestione dei cambiamenti",
"Test information":"Informazioni di test",
"Protection of information systems during audit testing":"Protezione dei sistemi durante test di audit",
}

def md_header(title, lang):
    if lang=="it":
        return f"# {title}\n\n> Versione: {today}  \n> Proprietario: Andrea Gagliardi\n\n"
    return f"# {title}\n\n> Version: {today}  \n> Owner: Andrea Gagliardi\n\n"

# --- Context docs (IT/EN)
scope_it = md_header("Campo di applicazione (Scope) ISMS", "it") + textwrap.dedent("""\
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
""")

scope_en = md_header("ISMS Scope", "en") + textwrap.dedent("""\
## Organization
Auctory (software startup).

## Scope
The ISMS covers the **design, development, release and operational management** of **Auctory SaaS** solutions for industrial data acquisition and processing, hosted on **customer-dedicated cloud VMs** at Hetzner.

## In scope
- GitHub repositories and development pipelines (code, IaC, CI/CD, operational documentation).
- Segregated environments: **dev / staging / prod**.
- Customer-dedicated cloud infrastructure (VMs, networking, firewalling, storage).
- Remote administration via authenticated overlay/SDN network.
- Centralized system and application logging via syslog.
- Customer setup metrics/monitoring via Prometheus.

## Out of scope
- Physical infrastructure (Auctory does not operate a datacenter).
- Customer on-prem systems unless explicitly contracted.
- Hardware gateways: out of scope; fleet management is delegated to Balena Cloud (ISO 27001 certified provider).

## Logical boundaries
- Primary segregation through **one dedicated VM set per customer**.
- Administrative access only via authenticated overlay network + MFA with hardware security keys.

## Dependencies
- Hetzner provides VM snapshot/backup capabilities; Auctory defines policy, retention and restore testing.
""")

# organization context + parties + objectives
orgctx_it = md_header("Contesto dell’organizzazione", "it") + textwrap.dedent("""\
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
""")

orgctx_en = md_header("Organization context", "en") + textwrap.dedent("""\
## Operating model
- Distributed team (remote-first), 3 people with infrastructure access.
- Main tooling: GitHub, Hetzner Cloud, overlay network (e.g., Tailscale) for administrative access.
- Architecture: customer-dedicated VMs (strong segregation).

## Information types
- Industrial operational data (telemetry/production).
- System and application logs.
- Infrastructure configuration data (IaC, secrets handled per policy).

## Security objectives
Protect confidentiality, integrity and availability of:
- customer systems and data within the Auctory perimeter,
- source code and CI/CD pipelines,
- credentials and cryptographic keys,
- ISMS documentation and records.
""")

parties_it = md_header("Parti interessate e requisiti", "it") + textwrap.dedent("""\
## Parti interessate
- Clienti (industriali, spesso enterprise)
- Auctory (management e team tecnico)
- Fornitori critici (Hetzner, GitHub, overlay network provider, Balena)
- Autorità/regolatori (es. GDPR in UE)

## Requisiti principali
- Confidenzialità e segregazione per cliente
- Tracciabilità (audit trail) e change management
- Continuità operativa (backup/restore testati)
- Gestione incidenti con tempi di reazione adeguati
- Secure SDLC (code review, vulnerability mgmt)
""")

parties_en = md_header("Interested parties and requirements", "en") + textwrap.dedent("""\
## Interested parties
- Customers (industrial, often enterprise)
- Auctory (management and engineering)
- Critical suppliers (Hetzner, GitHub, overlay network provider, Balena)
- Authorities/regulators (e.g., GDPR in the EU)

## Key requirements
- Customer segregation and confidentiality
- Traceability (audit trail) and change management
- Business continuity (tested backup/restore)
- Incident management with appropriate response times
- Secure SDLC (code review, vulnerability management)
""")

objectives_it = md_header("Obiettivi ISMS e KPI", "it") + textwrap.dedent("""\
## Obiettivi (annuali)
1. **Zero accessi amministrativi senza MFA** (target 100%).
2. **Restore test completato e registrato** per almeno 1 istanza campione/anno.
3. **Patch & vulnerability management**: tutte le vulnerabilità critiche gestite entro SLA interno.
4. **Incident response**: classificazione evento entro 24h, containment secondo runbook.
5. **Auditability**: 100% dei cambiamenti a produzione via PR/Change record.

## KPI suggeriti
- % MFA enforcement (GitHub/Hetzner/overlay)
- Tempo medio ripristino (restore test)
- MTTR incidenti critici
- Tempo medio di patching per CVE High/Critical
- Numero eccezioni di accesso privilegiato approvate
""")

objectives_en = md_header("ISMS objectives and KPIs", "en") + textwrap.dedent("""\
## Annual objectives
1. **No administrative access without MFA** (target 100%).
2. **Restore test completed and recorded** for at least one sample instance per year.
3. **Patch & vulnerability management**: all critical vulnerabilities handled within internal SLA.
4. **Incident response**: event triage within 24h, containment per runbook.
5. **Auditability**: 100% of production changes via PR/Change record.

## Suggested KPIs
- % MFA enforcement (GitHub/Hetzner/overlay)
- Mean restore time (restore test)
- MTTR for critical incidents
- Mean patch time for High/Critical CVEs
- # privileged access exceptions approved
""")

# Governance docs
policy_it = md_header("Politica per la Sicurezza delle Informazioni", "it") + textwrap.dedent("""\
## Impegno della direzione
La direzione di Auctory si impegna a:
- proteggere le informazioni e i servizi erogati ai clienti secondo i principi CIA (Confidenzialità, Integrità, Disponibilità);
- soddisfare requisiti legali e contrattuali applicabili (incluso GDPR dove rilevante);
- definire obiettivi misurabili e promuovere il miglioramento continuo dell’ISMS;
- garantire che ruoli e responsabilità siano chiari e che le risorse necessarie siano disponibili.

## Principi operativi
- **Security-by-default** e **least privilege**.
- **ISMS-as-Code**: documentazione e registri gestiti tramite versioning e workflow Git.
- **Segregazione per cliente**: VM dedicate e controllo accessi.
- **MFA obbligatoria** e preferenza per hardware keys (Yubikey).
- Logging, monitoraggio e gestione incidenti come processi standard.

## Approvazione
Approvata da: Andrea Gagliardi (Top Management / ISMS Manager)  
Data: {today}
""").format(today=today)

policy_en = md_header("Information Security Policy", "en") + textwrap.dedent("""\
## Management commitment
Auctory management commits to:
- protect customer information and services according to CIA principles (Confidentiality, Integrity, Availability);
- meet applicable legal and contractual requirements (including GDPR where relevant);
- define measurable objectives and continuously improve the ISMS;
- ensure clear roles/responsibilities and adequate resources.

## Operating principles
- **Security-by-default** and **least privilege**.
- **ISMS-as-Code**: documentation and registers maintained via Git versioning and workflow.
- **Customer segregation**: dedicated VMs and access control.
- **Mandatory MFA** with preference for hardware security keys (Yubikey).
- Logging, monitoring and incident management as standard processes.

## Approval
Approved by: Andrea Gagliardi (Top Management / ISMS Manager)  
Date: {today}
""").format(today=today)

roles_it = md_header("Ruoli e responsabilità", "it") + textwrap.dedent("""\
## Struttura minima (startup)
- **Top Management**: Andrea Gagliardi
- **ISMS Manager**: Andrea Gagliardi
- **System/Cloud Owners**: team tecnico (designato per attività)
- **Developers**: team Auctory

## Responsabilità chiave
### Top Management / ISMS Manager
- Approvare policy, scope, obiettivi.
- Approvare Risk Assessment, Risk Treatment Plan e SoA.
- Pianificare e condurre Management Review annuale.
- Approvare azioni correttive e miglioramenti.

### Team tecnico (operazioni)
- Gestione accessi e privilegi.
- Gestione backup/restore e test.
- Logging/monitoring e gestione incidenti.
- Gestione cambi (change management) e release.

### Tutti
- Segnalare eventi di sicurezza.
- Rispettare policy e procedure.
""")

roles_en = md_header("Roles and responsibilities", "en") + textwrap.dedent("""\
## Minimal structure (startup)
- **Top Management**: Andrea Gagliardi
- **ISMS Manager**: Andrea Gagliardi
- **System/Cloud Owners**: engineering team (assigned per activity)
- **Developers**: Auctory team

## Key responsibilities
### Top Management / ISMS Manager
- Approve policy, scope, objectives.
- Approve Risk Assessment, Risk Treatment Plan and SoA.
- Plan and perform annual Management Review.
- Approve corrective actions and improvements.

### Engineering (operations)
- Access and privilege management.
- Backup/restore and testing.
- Logging/monitoring and incident handling.
- Change management and releases.

### Everyone
- Report security events.
- Follow policies and procedures.
""")

docctrl_it = md_header("Procedura di controllo documenti (ISMS-as-Code)", "it") + textwrap.dedent("""\
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
""")

docctrl_en = md_header("Document control procedure (ISMS-as-Code)", "en") + textwrap.dedent("""\
## Purpose
Ensure ISMS documentation is controlled, updated, approved and traceable.

## Rules
- All ISMS documents live in this Git repository.
- Changes are made via **Pull Request** with mandatory review.
- Recommended branch protection:
  - PR required
  - at least 1 reviewer
  - status checks (CI) where applicable
- Each document includes a date/version in its header.
- After the annual Management Review, create a **release tag** (e.g. `ISMS-2026-v1.0`).

## Retention
- Git history is the versioning record.
- Repository backup per provider policy (GitHub) + optional periodic export.
""")

mgmtrev_it = md_header("Procedura di Management Review", "it") + textwrap.dedent("""\
## Frequenza
Annuale (o straordinaria in caso di incidenti maggiori / cambi significativi).

## Input minimi
- Stato azioni da audit interni e precedenti review
- KPI e metriche (MFA enforcement, restore test, incidenti, patching)
- Stato rischi (nuovi rischi, variazioni, accettazioni)
- Stato fornitori critici e variazioni contrattuali
- Cambi significativi in architettura/prodotti

## Output
- Decisioni e azioni di miglioramento (con owner e scadenza)
- Aggiornamento obiettivi ISMS
- Aggiornamento SoA e Risk Treatment Plan se necessario
- Tag release del repository ISMS
""")

mgmtrev_en = md_header("Management Review procedure", "en") + textwrap.dedent("""\
## Frequency
Annually (or ad-hoc after major incidents / significant changes).

## Minimum inputs
- Status of actions from internal audits and previous reviews
- KPIs (MFA enforcement, restore test, incidents, patching)
- Risk status (new risks, changes, acceptances)
- Critical suppliers status and contractual changes
- Significant changes in architecture/products

## Outputs
- Improvement decisions and actions (owner + due date)
- Updated ISMS objectives
- Updates to SoA and Risk Treatment Plan if needed
- ISMS repository release tag
""")

# Risk management docs
risk_method_it = md_header("Metodologia di Risk Assessment", "it") + textwrap.dedent("""\
## Scopo
Valutare e trattare i rischi per la sicurezza delle informazioni nel perimetro ISMS.

## Metodo
Scala 1–3 per Likelihood (L) e Impact (I). Risk Score = L × I.

### Likelihood (L)
1. Improbabile
2. Possibile
3. Probabile

### Impact (I)
1. Basso (impatto limitato, ripristino rapido)
2. Medio (interruzione/violazione con impatti significativi)
3. Alto (impatto su clienti enterprise, perdita dati, downtime significativo, impatti legali)

### Soglie
- 1–2: basso (monitorare)
- 3–4: medio (trattare se costo/beneficio favorevole)
- 6–9: alto (trattamento obbligatorio)

## Frequenza
- Riesame rischi: almeno annuale, e dopo cambi significativi o incidenti maggiori.

## Output obbligatori
- Risk Register
- Risk Treatment Plan
- SoA allineata al trattamento del rischio
""")

risk_method_en = md_header("Risk assessment methodology", "en") + textwrap.dedent("""\
## Purpose
Assess and treat information security risks within the ISMS scope.

## Method
1–3 scale for Likelihood (L) and Impact (I). Risk Score = L × I.

### Likelihood (L)
1. Unlikely
2. Possible
3. Likely

### Impact (I)
1. Low (limited impact, quick recovery)
2. Medium (meaningful service disruption/breach)
3. High (enterprise customer impact, data loss, significant downtime, legal impact)

### Thresholds
- 1–2: low (monitor)
- 3–4: medium (treat where cost-effective)
- 6–9: high (treatment required)

## Frequency
- Risk review at least annually and after significant changes or major incidents.

## Mandatory outputs
- Risk Register
- Risk Treatment Plan
- SoA aligned to risk treatment
""")

risk_treat_it = md_header("Piano di trattamento del rischio", "it") + textwrap.dedent("""\
## Principi
Per ciascun rischio:
- evitare / ridurre / trasferire / accettare
- definire controlli, owner, scadenza, evidenze

Il dettaglio operativo è mantenuto in `03_risk_management/risk_register.yaml`.
""")

risk_treat_en = md_header("Risk treatment plan", "en") + textwrap.dedent("""\
## Principles
For each risk:
- avoid / reduce / transfer / accept
- define controls, owner, due date, evidence

Operational detail is maintained in `03_risk_management/risk_register.yaml`.
""")

# Controls docs (IT/EN) - concise but strong
access_it = md_header("Politica di controllo accessi", "it") + textwrap.dedent("""\
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
""")

access_en = md_header("Access control policy", "en") + textwrap.dedent("""\
## Principles
- Least privilege, need-to-know, separation of duties where applicable.
- Mandatory MFA for all critical accounts (GitHub, Hetzner, overlay network).
- Preference for hardware security keys (Yubikey/passkeys).

## Privileged access
- Root/admin access only when operationally required.
- All privileged access must be logged and recorded in `privileged_access_register.yaml`.

## Identity management (high level)
- Onboarding: account creation, role assignment, MFA enablement.
- Offboarding: access revocation, key/secret rotation, session termination.

## Infrastructure access
- Administrative access to VMs only through overlay network + MFA.
- SSH key auth; disable SSH passwords where possible.
""")

crypto_it = md_header("Politica crittografica", "it") + textwrap.dedent("""\
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
""")

crypto_en = md_header("Cryptography policy", "en") + textwrap.dedent("""\
## Objective
Protect data in transit and, where applicable, at rest.

## Guidelines
- TLS for application/API traffic.
- SSH key-based access.
- Full disk encryption on user endpoints.
- Key management:
  - protect private keys (hardware keys where feasible)
  - rotate keys after incidents/offboarding

## Secrets
- Secrets/tokens MUST NOT be committed to the repo.
- Use secret managers / CI/CD variables / vault according to product architecture.
""")

sdlc_it = md_header("Politica Secure Development", "it") + textwrap.dedent("""\
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
""")

sdlc_en = md_header("Secure development policy", "en") + textwrap.dedent("""\
## Workflow
- All changes via Pull Request.
- Mandatory code review.
- Branch protection (main/prod): merge only with review and checks.

## Vulnerability management
- Dependency scanning (e.g., Dependabot) enabled.
- High/Critical vulnerabilities: handled within internal SLA and tracked via issues.

## Environment separation
- Dev/Staging/Prod separated (control 8.31).
- Production data not used in dev/test unless anonymized or explicitly authorized.

## Source code access
- Role-based access; private repositories as needed.
- GitHub audit trail enabled.
""")

change_it = md_header("Procedura di Change Management", "it") + textwrap.dedent("""\
## Scopo
Garantire che i cambi a produzione siano autorizzati, testati e tracciabili.

## Regole
- Ogni change a produzione richiede:
  - ticket/issue o change record
  - PR con review
  - evidenza test (staging) ove applicabile
- Deploy: preferibilmente automatizzato (CI/CD) con log dei rilasci.
- Rollback: definire strategia per componente (documentare nei runbook di servizio).
""")

change_en = md_header("Change management procedure", "en") + textwrap.dedent("""\
## Purpose
Ensure production changes are authorized, tested and traceable.

## Rules
- Every production change requires:
  - ticket/issue or change record
  - PR with review
  - test evidence (staging) where applicable
- Deploy: preferably automated (CI/CD) with release logs.
- Rollback: define per-component strategy (document in service runbooks).
""")

backup_it = md_header("Politica backup e restore", "it") + textwrap.dedent("""\
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
""")

backup_en = md_header("Backup and restore policy", "en") + textwrap.dedent("""\
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
""")

logmon_it = md_header("Politica logging e monitoring", "it") + textwrap.dedent("""\
## Logging
- Logging centralizzato sistemistico e applicativo per ogni setup cliente basato su syslog.
- Retention e accesso ai log definiti per classe cliente e requisiti legali/contrattuali.
- Protezione log: accesso ristretto, integrità (immutabilità dove possibile).

## Monitoring
- Ogni setup cliente dispone di server metriche basato su Prometheus.
- Alerting su eventi critici (es. saturazione storage, down servizi, anomalie).

## Uso in incident response
- I log e le metriche supportano detection, triage, containment e post-mortem.
""")

logmon_en = md_header("Logging and monitoring policy", "en") + textwrap.dedent("""\
## Logging
- Centralized system and application logging per customer setup via syslog.
- Log retention and access defined per customer tier and legal/contractual requirements.
- Log protection: restricted access, integrity (immutability where feasible).

## Monitoring
- Each customer setup includes a Prometheus-based metrics server.
- Alerting for critical events (e.g., storage saturation, service down, anomalies).

## Use in incident response
- Logs and metrics support detection, triage, containment and post-mortem.
""")

irp_it = md_header("Piano di risposta agli incidenti", "it") + textwrap.dedent("""\
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
""")

irp_en = md_header("Incident response plan", "en") + textwrap.dedent("""\
## Definitions
- **Event**: observable occurrence.
- **Incident**: event impacting (or potentially impacting) security (CIA) or involving a breach.

## Phases
1. Preparation (runbooks, contacts, access, tooling)
2. Identification & triage (within 24h)
3. Containment (limit impact)
4. Eradication & recovery
5. Lessons learned (post-mortem) and updates to risk/controls

## Recording
- Every incident is recorded in `incident_register.yaml`.
- Evidence stored under `evidence/` (redacted when needed).
""")

bcp_it = md_header("Business Continuity Plan (BCP) - Sintesi", "it") + textwrap.dedent("""\
## Obiettivo
Garantire continuità minima dei servizi SaaS Auctory e ripristino entro target (RTO/RPO).

## Scenari
- indisponibilità VM/region provider
- perdita dati / corruzione
- compromissione credenziali
- indisponibilità team (remote)

## Strategie
- backup/snapshot e restore test
- procedure di key rotation e access recovery
- runbook di ripristino servizi e comunicazione clienti
""")

bcp_en = md_header("Business Continuity Plan (BCP) - Summary", "en") + textwrap.dedent("""\
## Objective
Ensure minimum continuity of Auctory SaaS services and recovery within targets (RTO/RPO).

## Scenarios
- VM/provider region outage
- data loss/corruption
- credential compromise
- team unavailability (remote)

## Strategies
- backup/snapshot and restore testing
- key rotation and access recovery procedures
- service restoration and customer communication runbooks
""")

supplier_it = md_header("Politica sicurezza fornitori", "it") + textwrap.dedent("""\
## Fornitori critici (tipici)
- Hetzner (cloud)
- GitHub (code + audit trail)
- Overlay network provider (es. Tailscale)
- Balena Cloud (out of scope per gateway, ma dipendenza di servizio)

## Requisiti
- Registro fornitori: `supplier_register.yaml`
- Valutazione rischio iniziale e riesame annuale
- Monitoraggio cambi contrattuali / incidenti noti
- Clausole minime: riservatezza, disponibilità, notifica incidenti (dove possibile)
""")

supplier_en = md_header("Supplier security policy", "en") + textwrap.dedent("""\
## Critical suppliers (typical)
- Hetzner (cloud)
- GitHub (code + audit trail)
- Overlay network provider (e.g., Tailscale)
- Balena Cloud (out-of-scope for gateways, but service dependency)

## Requirements
- Supplier register: `supplier_register.yaml`
- Initial risk assessment and annual review
- Monitor contractual changes / known incidents
- Minimum clauses: confidentiality, availability, incident notification (where feasible)
""")

asset_it = md_header("Politica gestione asset", "it") + textwrap.dedent("""\
## Inventario
Gli asset in scope sono mantenuti in `asset_register.yaml` e includono:
- account e sistemi critici (GitHub org, Hetzner, overlay network)
- VM per-cliente e componenti principali
- sistemi di logging/monitoring

## Classificazione
Ogni asset ha una classificazione (Low/Medium/High) e un owner.

## Ciclo di vita
Onboarding / modifica / dismissione con tracciabilità (issue + PR quando applicabile).
""")

asset_en = md_header("Asset management policy", "en") + textwrap.dedent("""\
## Inventory
In-scope assets are maintained in `asset_register.yaml` and include:
- critical accounts/systems (GitHub org, Hetzner, overlay network)
- customer-dedicated VMs and key components
- logging/monitoring systems

## Classification
Each asset has a classification (Low/Medium/High) and an owner.

## Lifecycle
Onboarding / change / decommission with traceability (issue + PR where applicable).
""")

# Registers YAML
write("03_risk_management/risk_register.yaml", textwrap.dedent("""\
# Auctory Risk Register (starter)
# Fields are intentionally explicit to support audits.
- id: R-001
  title: Compromise of GitHub Organization account
  asset: GitHub Organization
  threat: Account takeover / token theft
  likelihood: 1
  impact: 3
  risk_score: 3
  treatment_decision: Reduce
  controls:
    - "5.15"
    - "5.16"
    - "5.17"
    - "8.4"
    - "8.5"
  current_measures: "MFA enforced; hardware security keys (Yubikey); branch protection; audit logs."
  action_plan: "Maintain MFA enforcement; review org members quarterly; enable dependency scanning."
  owner: "Andrea Gagliardi"
  due_date: "2026-06-30"
  status: "Implemented"
  evidence:
    - "evidence/screenshots/github-mfa-enforcement.png (placeholder)"
- id: R-002
  title: Customer VM data loss without timely recovery
  asset: Customer-dedicated Hetzner VM(s)
  threat: Storage failure / operator error / corruption
  likelihood: 2
  impact: 3
  risk_score: 6
  treatment_decision: Reduce
  controls:
    - "8.13"
    - "5.30"
  current_measures: "Hetzner snapshots/backups available; restore procedure documented."
  action_plan: "Define RPO/RTO per tier; perform and record annual restore test."
  owner: "Andrea Gagliardi"
  due_date: "2026-05-31"
  status: "In progress"
  evidence:
    - "evidence/restore-tests/restore-test-2026-01.md (placeholder)"
"""))

write("05_registers/asset_register.yaml", textwrap.dedent("""\
# Asset Register (starter)
- id: AS-001
  name: GitHub Organization (Auctory)
  type: SaaS Platform
  owner: "Andrea Gagliardi"
  classification: High
  notes: "Source code, CI/CD, ISMS docs, audit trail."

- id: AS-002
  name: Hetzner Cloud Account
  type: Cloud Provider Account
  owner: "Andrea Gagliardi"
  classification: High
  notes: "Customer-dedicated VMs, snapshots/backups."

- id: AS-003
  name: Overlay Network (e.g., Tailscale)
  type: Network Access Control
  owner: "Andrea Gagliardi"
  classification: High
  notes: "Admin access path to customer VMs; MFA enforced."

- id: AS-004
  name: Centralized syslog (per customer)
  type: Logging Service
  owner: "Engineering"
  classification: High
  notes: "System and application logs; retention per customer tier."

- id: AS-005
  name: Prometheus metrics server (per customer)
  type: Monitoring Service
  owner: "Engineering"
  classification: Medium
  notes: "Metrics and alerting."
"""))

write("05_registers/supplier_register.yaml", textwrap.dedent("""\
# Supplier Register (starter)
- id: SUP-001
  name: Hetzner
  service: Cloud VMs + snapshot/backup capability
  criticality: High
  iso27001_certified: "Unknown/To verify"
  review_frequency: Annual
  notes: "Customer-dedicated infrastructure; key dependency."
- id: SUP-002
  name: GitHub
  service: Source control + CI/CD + audit trail
  criticality: High
  iso27001_certified: "Unknown/To verify"
  review_frequency: Annual
  notes: "ISMS-as-Code repository lives here."
- id: SUP-003
  name: Overlay network provider (e.g., Tailscale)
  service: SDN overlay for admin access
  criticality: High
  iso27001_certified: "Unknown/To verify"
  review_frequency: Annual
  notes: "Primary path for administrative access."
- id: SUP-004
  name: Balena Cloud
  service: Fleet management (out of ISMS scope for gateways)
  criticality: Medium
  iso27001_certified: "Yes (provider claim) / To verify"
  review_frequency: Annual
  notes: "Dependency for gateway management; gateway out-of-scope."
"""))

write("05_registers/privileged_access_register.yaml", textwrap.dedent("""\
# Privileged Access Register (starter)
- id: PA-2026-0001
  date: "2026-02-01"
  system: "Hetzner VM - Customer A"
  requester: "Andrea Gagliardi"
  reason: "Planned maintenance / security patching"
  approval: "Andrea Gagliardi"
  duration: "2h"
  evidence: "Link to issue/PR and logs (placeholder)"
"""))

write("05_registers/incident_register.yaml", textwrap.dedent("""\
# Incident Register (starter)
- id: INC-2026-0001
  date_detected: "2026-01-15"
  detected_by: "Monitoring"
  description: "Example placeholder - remove once real incidents exist."
  severity: "Low"
  status: "Closed"
  actions_taken: "N/A"
  lessons_learned: "N/A"
  evidence: "N/A"
"""))

write("05_registers/backup_test_register.yaml", textwrap.dedent("""\
# Backup restore test register (starter)
- id: BRT-2026-0001
  date: "2026-01-20"
  system: "Hetzner VM - Sample customer instance"
  backup_type: "Snapshot"
  rto_achieved: "TBD"
  rpo_achieved: "TBD"
  outcome: "Success"
  performed_by: "Engineering"
  evidence: "evidence/restore-tests/restore-test-2026-01.md (placeholder)"
"""))

# Statement of Applicability YAML
soa_lines = []
soa_lines.append("# Statement of Applicability (SoA) - ISO/IEC 27001:2022 Annex A")
soa_lines.append("# Controls list and titles aligned to ISO/IEC 27001:2022 Annex A structure (93 controls).")
soa_lines.append("controls:")
for cid, en_name in controls:
    it_name = it_map.get(en_name, en_name)
    soa_lines.append(f"  - id: \"{cid}\"")
    soa_lines.append(f"    name_en: \"{en_name}\"")
    soa_lines.append(f"    name_it: \"{it_name}\"")
    soa_lines.append("    applicable: true")
    soa_lines.append("    implementation_status: \"Implemented\"  # Implemented | Planned | Not implemented")
    soa_lines.append("    justification: \"\"  # why applicable/not applicable, based on scope & risks")
    soa_lines.append("    control_owner: \"Andrea Gagliardi\"")
    soa_lines.append("    references:")
    soa_lines.append("      - \"\"  # e.g., link to policy/procedure in this repo")
    soa_lines.append("    evidence:")
    soa_lines.append("      - \"\"  # e.g., evidence path or immutable link")
write("06_annex_a/statement_of_applicability.yaml", "\n".join(soa_lines) + "\n")

# Create language files
for lang in langs:
    root = pathlib.Path(lang)
    # context
    write(f"{lang}/01_context/scope.md", scope_it if lang=="it" else scope_en)
    write(f"{lang}/01_context/organization_context.md", orgctx_it if lang=="it" else orgctx_en)
    write(f"{lang}/01_context/interested_parties.md", parties_it if lang=="it" else parties_en)
    write(f"{lang}/01_context/isms_objectives.md", objectives_it if lang=="it" else objectives_en)
    # governance
    write(f"{lang}/02_governance/information_security_policy.md", policy_it if lang=="it" else policy_en)
    write(f"{lang}/02_governance/roles_and_responsibilities.md", roles_it if lang=="it" else roles_en)
    write(f"{lang}/02_governance/document_control_procedure.md", docctrl_it if lang=="it" else docctrl_en)
    write(f"{lang}/02_governance/management_review_procedure.md", mgmtrev_it if lang=="it" else mgmtrev_en)
    # risk mgmt
    write(f"{lang}/03_risk_management/risk_assessment_methodology.md", risk_method_it if lang=="it" else risk_method_en)
    write(f"{lang}/03_risk_management/risk_treatment_plan.md", risk_treat_it if lang=="it" else risk_treat_en)
    # controls
    write(f"{lang}/04_controls/access_control_policy.md", access_it if lang=="it" else access_en)
    write(f"{lang}/04_controls/cryptography_policy.md", crypto_it if lang=="it" else crypto_en)
    write(f"{lang}/04_controls/secure_development_policy.md", sdlc_it if lang=="it" else sdlc_en)
    write(f"{lang}/04_controls/change_management_procedure.md", change_it if lang=="it" else change_en)
    write(f"{lang}/04_controls/backup_and_restore_policy.md", backup_it if lang=="it" else backup_en)
    write(f"{lang}/04_controls/logging_and_monitoring_policy.md", logmon_it if lang=="it" else logmon_en)
    write(f"{lang}/04_controls/incident_response_plan.md", irp_it if lang=="it" else irp_en)
    write(f"{lang}/04_controls/business_continuity_plan.md", bcp_it if lang=="it" else bcp_en)
    write(f"{lang}/04_controls/supplier_security_policy.md", supplier_it if lang=="it" else supplier_en)
    write(f"{lang}/04_controls/asset_management_policy.md", asset_it if lang=="it" else asset_en)

# Zip it
zip_path = pathlib.Path("auctory-isms-bootstrap.zip")
if zip_path.exists():
    zip_path.unlink()

with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as z:
    for p in base.rglob("*"):
        if p.is_file():
            z.write(p, arcname=str(p.relative_to(base)))

zip_path, sum(1 for _ in base.rglob("*") if _.is_file())

