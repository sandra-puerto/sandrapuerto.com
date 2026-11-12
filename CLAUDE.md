# CLAUDE.md — Landing SGPT Guidelines & Architecture Directives

> **«Aislamiento por diseño, no por disciplina»** — *(“Isolation by design, not by discipline”)*

## Repository Overview
`landing-sgpt` (`sandrapuerto.com`) is a high-performance, zero-dependency static web delivery service engineered under the **Stratum Sovereign Consumer Pattern (v2.0)**. It serves the professional portfolio of **Sandra Gabriela Puerto Torres** using hardened Nginx (`nginx:latest` for unattended operation) and vanilla HTML5, CSS3, and ES6+.

## Architectural Constraints
1. **Network Boundary & Zero Host Ports:**
   - Exposes zero ports on the physical host (`0.0.0.0` unbound).
   - Attaches to an external Stratum network via `${STRATUM_NETWORK}` (`stratum_dmz` or `stratum_${TENANT_ORG}_internal`).
   - Provides dual DNS aliases (`landing-sgpt-web` and `stratum-app-${TENANT_ORG:-sgpt}-web`).
2. **Hardening & Performance:**
   - Immutable root filesystem (`read_only: true`) with volatile `tmpfs` mounts (`/var/cache/nginx`, `/var/run`, `/tmp`).
   - `no-new-privileges: true`, `cap_drop: [ALL]`, and strict resource quotas (`mem_limit: 128m`, `pids_limit: 100`).
   - Out-of-tree error and maintenance templates (`templates/404.html`, `templates/maintenance.html`).
   - Strict HTTP method filtering (`GET`, `HEAD`, `OPTIONS` only -> `405` otherwise) and dotfiles/sensitive extension blocking (`404`).
3. **Immutable Asset Cache-Busting:**
   - Static assets are served with `Cache-Control: public, max-age=31536000, immutable`.
   - Any change to `public/css/styles.css` or `public/js/app.js` requires running `python scripts/version_assets.py`.

## Validation Commands
```bash
# 1. Refresh and verify asset cache-busting hashes:
python scripts/version_assets.py
python scripts/version_assets.py --check

# 2. Validate Docker Compose configuration:
cp .env.example .env
docker compose config --quiet

# 3. Validate Nginx configuration syntax:
docker run --rm \
  -v "$PWD/nginx/nginx.conf:/etc/nginx/nginx.conf:ro" \
  -v "$PWD/nginx/conf.d:/etc/nginx/conf.d:ro" \
  -v "$PWD/public:/usr/share/nginx/html:ro" \
  -v "$PWD/templates:/usr/share/nginx/templates:ro" \
  nginx:latest nginx -t
```

## Attribution & Legal
- **Author & Architect:** Sandra Gabriela Puerto Torres (`https://sandrapuerto.com`)
- **Pattern:** Stratum Sovereign Consumer (v2.0.0)
