# Security Awareness Lab

A public skeleton for an authorized phishing-awareness project: architecture, governance, neutral educational content and fictional sample data.

**Status:** portfolio scaffold. No email delivery, tracking, credential collection, live campaign or public deployment is implemented.

## What is reused

The project organization separates configuration, infrastructure, training content, participant data and reporting. All public files were written afresh. There is no private source history, branding, operational identifier, recipient list, campaign result or credential in this repository.

## Structure

```text
config/lab.example.json          Documentation-only settings
docs/architecture.md            Components and trust boundaries
docs/campaign-runbook.md         Planning, approval and closure
docs/privacy-and-metrics.md      Data minimization and metrics
cloudflared/README.md            Optional tunnel integration boundary
nginx/README.md                  Optional proxy integration boundary
landing/index.html              Neutral educational preview
templates/email.example.html    Clearly labeled email mockup
data/participants.example.csv   One fictional participant
examples/aggregate-metrics.json Fabricated aggregate report
scripts/validate_skeleton.py    Local scaffold checks
SECURITY.md                     Publication and reporting policy
```

## Inspect locally

```sh
git clone https://github.com/Xilambila/security-awareness-lab.git
cd security-awareness-lab
python scripts/validate_skeleton.py
```

Python 3.11+ is sufficient; there are no external dependencies. Open the two HTML files directly in a browser for a static preview. No server, account or API key is needed.

The JSON documents scaffold intent; it is not a GoPhish, Nginx or Cloudflare runtime configuration. The checker validates selected structural and publication rules, not every possible secret.

## Security decisions represented

| Area | Decision | Evidence level |
|---|---|---|
| Governance | Approved scope, accountable owner and stop conditions | Runbook template |
| Infrastructure | Separate administration, least privilege and controlled ingress | Design notes |
| Privacy | Minimal data and aggregate reporting | Fictional fixtures |
| Learning | Neutral content without password forms or external assets | Static HTML |
| Publication | Fresh files and history; runtime data excluded | Scaffold and validation |

An operational version requires separate implementation and validation of access controls, delivery, privacy requirements, retention, monitoring and incident handling. No production outcome or campaign performance is claimed.

## Em português

Esqueleto público de um projeto de conscientização sobre phishing, com organização técnica, governança e privacidade. Os arquivos foram criados do zero; o original permanece privado. Esta versão não executa campanhas nem contém participantes reais.
