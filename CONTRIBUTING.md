# Contributing Guidelines

Contributions to **landing-sgpt** are welcomed. To maintain code quality, security standards, and performance benchmarks, adherence to the following guidelines is required.

---

## 1. Architectural Philosophy

This project strictly adheres to the **Stratum Consumer Architecture Pattern** and web standards:
* **Zero Dependencies:** No heavy build frameworks, node runtimes, or external bundlers inside the container.
* **Vanilla Standards:** HTML5 semantic markup, modern CSS3 (custom properties, Grid, Flexbox), and clean modular ES6+.
* **Container Hardening:** Containers must remain stateless, immutable (`read_only: true`), with minimal capabilities.

---

## 2. Development Workflow

1. **Fork the Repository:** Create a personal fork on GitHub.
2. **Create a Feature Branch:**
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Local Testing:**
   Test changes locally using an HTTP static server:
   ```bash
   python -m http.server 8000 -d public/
   ```
4. **Asset Validation:**
   Ensure HTML markup is valid and CSS adheres to the design tokens defined in `public/css/styles.css`.
5. **Cache Busting:**
   Run `python scripts/version_assets.py` after modifying any CSS/JS so HTML references get a new `?v=<hash>`. Verify with `python scripts/version_assets.py --check`. Never minify sources in place.
6. **Commit Standards:**
   Write clear, imperative commit messages (e.g., `feat(ui): add responsive container scaling`, `fix(nginx): update CSP font origins`).
7. **Submit a Pull Request:** Open a PR against the `main` branch with a clear description of the modifications.

---

## 3. Code Standards & Quality

* **HTML:** Maintain semantic hierarchy, descriptive ARIA attributes, and unique IDs for interactive nodes.
* **CSS:** Use custom properties declared in `:root` for typography, spacing, and color palettes. Avoid ad-hoc inline styles where classes exist.
* **JavaScript:** Write defensive, documented JSDoc code. Do not block DOM rendering.
* **Nginx Configuration:** Always verify `nginx -t` before committing configuration updates.

---

## 4. Code of Conduct

All contributors and maintainers are expected to maintain professional, respectful, and constructive collaboration.
