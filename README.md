# CyHelm Virtual CISO Policy Generator

A deterministic, review-first API that turns an organization profile into a tailored information security policy draft. It deliberately works without an external AI service so sensitive profile data can remain in the deployment boundary.

## MVP

- Validated organization questionnaire
- Context-aware information security policy sections
- Explicit draft status, review prompts, and human approval requirement
- OpenAPI interface ready for a web form or document-rendering adapter

## Quick start

```bash
docker compose up --build
curl -X POST http://localhost:8000/v1/policies/information-security \
  -H "Content-Type: application/json" \
  -d '{"name":"Example LLC","industry":"Professional Services","employees":30,"cloud_services":["Microsoft 365"]}'
```

Run locally with `pip install -e ".[dev]"`, then `uvicorn cyhelm.main:app --reload`.

## Production roadmap

Add versioned policy packs, approval workflow, DOCX/PDF renderers, jurisdiction-specific review prompts, immutable publication history, and optional private-model adapters. Never silently send policy inputs to an AI provider.

Generated policies are starting points—not legal advice, certification evidence, or a substitute for management approval.

