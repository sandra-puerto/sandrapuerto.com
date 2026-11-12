## Description

Brief summary of changes made to the landing page, static assets, or Nginx configuration.

## Type of Change

- [ ] Content or visual asset update (`public/`)
- [ ] Nginx server block or security headers tuning (`nginx/`)
- [ ] Stratum consumer topology or orchestration update (`docker-compose.yml`)
- [ ] CI/CD pipeline or workflow enhancements (`.github/`)
- [ ] Documentation update (`README.md`, `llms.txt`, etc.)

## Quality & Security Verification

- [ ] `python scripts/version_assets.py --check` passes with zero discrepancies.
- [ ] `docker compose config` validates cleanly against `.env.example`.
- [ ] Invariants respected: zero host ports published (`0.0.0.0`), read-only root filesystem, dropped capabilities.
- [ ] No secrets or sensitive configuration committed.
