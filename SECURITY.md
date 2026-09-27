# Security Policy

## 1. Supported Versions

Security updates and patches are actively applied to the following versions:

| Version | Supported          |
| :------ | :----------------- |
| 1.0.x   | :white_check_mark: |
| < 1.0.0 | :x:                |

---

## 2. Reporting a Vulnerability

Security is a foundational pillar of this infrastructure component. If you identify a potential security vulnerability, misconfiguration, or header bypass, please report it responsibly:

* **Direct Contact:** Send an email detailing the issue to the maintainer at **contacto@sandrapuerto.com** or via the contact points specified in [`public/humans.txt`](public/humans.txt).
* **Details to Include:**
  * Description of the vulnerability.
  * Steps or proof-of-concept (PoC) to reproduce the behavior.
  * Affected file(s) or Nginx directives.
  * Potential impact assessment.

Public GitHub issues for sensitive security vulnerabilities must not be opened until they have been reviewed and remediated.

---

## 3. Container & Web Hardening Baseline

This repository implements the following baseline hardening controls:
* Read-only container root filesystems (`read_only: true`).
* Total capability stripping (`cap_drop: [ALL]`) with minimal specific additions.
* Prevention of runtime privilege escalation (`no-new-privileges: true`).
* Ephemeral memory storage via `tmpfs` for caching, PID, and temporary file operations.
* Strict Content Security Policy (`Content-Security-Policy`), Clickjacking prevention (`X-Frame-Options: DENY`), and MIME sniffing prevention (`X-Content-Type-Options: nosniff`).
