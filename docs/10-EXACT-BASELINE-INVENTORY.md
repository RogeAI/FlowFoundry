# Exact Baseline Inventory

**Version:** 5.01
**Baseline date:** 11 October 2026
**Live reference:** localhost only (no external deployment configured)

---

## 1. Baseline Identity

| Item | Value |
|---|---|
| Product | FlowFoundry |
| Supervisor | ForgeMaster |
| Application version | `0.1.0` prototype |
| Documentation version | `5.00` |
| Python | `3.12+` |
| Framework/runtime | Django `5.2.17` LTS |
| Current routes | `/`, `/workspace/`, `/session/` |
| Current classification | Local Django simulation using the existing Python domain layer; no real Agent or external API execution |

---

## 2. Required Source Areas

```text
FlowFoundry/
├── flowfoundry/
├── web/
├── templates/web/
├── static/flowfoundry/
├── backend/
├── app/                 # retained React migration input
├── public/              # retained React assets
├── docs/
├── tests/
├── CLAUDE.md
├── PRODUCT-OVERVIEW.md
├── manage.py
└── requirements.txt
```

---

## 3. Final Primary Assets

| Asset | Purpose | Required property |
|---|---|---|
| `static/flowfoundry/images/flowfoundry-logo-modern-v1.png` | Current Django header logo | `2095 × 677`, transparent, ratio preserved |
| `static/flowfoundry/images/preview-forgemaster/` | ForgeMaster interface states | Transparent PNGs with proportions preserved |
| `static/flowfoundry/images/Athena.png`, `Hermes.png`, `Themis.png`, `Minerva.png`, and `Apolo.png` | Current Agent portraits | Individual transparent portrait assets |
| `static/flowfoundry/images/favicon.svg` | Browser icon | Referenced by the Django base template |

The `public/` copies remain for the retained React migration input. The current Django runtime serves its assets from `static/flowfoundry/images/`.

---

## 4. Reproduction Contract

A faithful reproduction requires:

1. using Python 3.12 or newer;
2. installing the root `requirements.txt`;
3. running `python manage.py migrate`;
4. running `python manage.py runserver 127.0.0.1:3001` from the directory containing `manage.py`;
5. preserving the static image assets and their displayed proportions;
6. viewing at the same browser width and 100% zoom when making visual comparisons.

---

## 5. Verification Record

The verified Django baseline passes `python manage.py check`, nine Django web tests, 37 retained backend/domain tests, JavaScript syntax checks, and browser walkthroughs of clarification, domain-enforced WFG/GO, Python-prepared planning, Working Session pause/resume, investigation, response, and completion.
