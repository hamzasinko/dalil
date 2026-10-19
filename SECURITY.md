# Security Policy

## Supported Versions

Dalil is in early development; only the latest release on PyPI receives
security fixes.

| Version | Supported |
|---------|-----------|
| 0.1.x   | ✅        |
| < 0.1   | ❌        |

## Reporting a Vulnerability

**Do not open a public issue for security vulnerabilities.**

Instead, please report them privately using one of these channels:

- GitHub Security Advisory: https://github.com/dalil-python/dalil/security/advisories/new
- Email: security@dalil.dev (placeholder — replace with a monitored address
  before launch)

Please include:

1. A description of the vulnerability and its impact.
2. Reproduction steps or a minimal proof of concept.
3. The affected version, Python version, and operating system.
4. Any known mitigations.

## What to expect

- We acknowledge reports within **72 hours**.
- We will keep you informed of the progress toward a fix.
- We will coordinate the disclosure: a fix is released first, then a public
  advisory and changelog entry are published.
- Credit is given to reporters who wish to be acknowledged, unless they prefer
  to remain anonymous.

## Scope

In scope: the `dalil` package itself (code execution, tracing, templates,
exports) and this repository's CI/CD configuration.

Out of scope: vulnerabilities in third-party dependencies (report them
upstream), denial-of-service against public infrastructure, and social
engineering.
