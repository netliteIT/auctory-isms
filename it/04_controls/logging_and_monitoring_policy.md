# Politica logging e monitoring

> Versione: 2026-02-26  
> Proprietario: Andrea Gagliardi

## Logging
- Logging centralizzato sistemistico e applicativo per ogni setup cliente basato su syslog.
- Retention e accesso ai log definiti per classe cliente e requisiti legali/contrattuali.
- Protezione log: accesso ristretto, integrità (immutabilità dove possibile).

## Monitoring
- Ogni setup cliente dispone di server metriche basato su Prometheus.
- Alerting su eventi critici (es. saturazione storage, down servizi, anomalie).

## Uso in incident response
- I log e le metriche supportano detection, triage, containment e post-mortem.
