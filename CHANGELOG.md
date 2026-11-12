# Changelog

All notable changes to `landing-sgpt` (`sandrapuerto.com`) are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [2.0.0] - 2026-11-12

### Added
- **Stratum v2.0 Integration:** Standardized container naming (`stratum-app-${TENANT_ORG:-sgpt}-web`), OCI labels (`com.stratum-core.*`), and dual network alias resolution (`landing-sgpt-web` and `stratum-app-sgpt-web`) for seamless routing via `stratum-cli`.
- **Flexible Network Topology:** Added `${STRATUM_NETWORK}` support to attach either to `stratum_dmz` (Perimeter Consumer) or `stratum_${TENANT_ORG}_internal` (Tier 3 Organization Island).
- **CI/CD Pipeline (`.github/workflows/ci.yml`):** Automated Docker Compose specification validation, asset fingerprint verification (`version_assets.py --check`), Nginx syntax testing (`nginx -t`), live runtime smoke & security tests, and continuous deployment trigger.
- **Python Tech Icon:** Added official vector icon `public/icons/tech/python.svg` and brand hover rules in `public/css/styles.css`.
- **Repository Governance:** Added `.gitattributes`, `.cursorrules`, `CLAUDE.md`, `CODE_OF_CONDUCT.md`, `CHANGELOG.md`, and `.github/PULL_REQUEST_TEMPLATE.md` aligned with the Stratum Group standards.

### Changed
- **Unattended Docker Image Tagging:** Replaced pinned SHA digest with `${NGINX_IMAGE:-nginx:latest}` and updated container healthcheck to `curl` for unattended lifecycle management.
- **Portfolio Content & CV Overhaul:** Updated all site copy, structured data (`Schema.org JSON-LD`), Open Graph banners (`og-image.png`), `llms.txt`, `humans.txt`, `manifest.json`, and downloadable PDF (`public/docs/cv-sandra-puerto.pdf`) to reflect the **Desarrolladora Backend Junior | SQL y Automatización de Procesos | Tecnóloga SENA COPNIA** profile.
- **Visual Clarity:** Removed full-viewport `#noise-overlay` SVG turbulence filter from `public/index.html`, `templates/404.html`, and `public/css/styles.css`.

---

## [1.0.2] - 2026-10-24

### Added
- Initial production release of the static web delivery service under the Stratum Consumer pattern with hardened Nginx configuration, immutable asset caching, and out-of-tree error/maintenance templates.
