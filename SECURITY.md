# Security Policy

## Supported versions

The following versions of this project receive security updates:

| Version | Supported          |
|---------|--------------------|
| `main`  | ✅ Active          |
| latest tagged release | ✅ Active |
| older releases | ❌ Best-effort only |

## Reporting a vulnerability

**Please do not open a public GitHub issue for security vulnerabilities.**

Instead, report privately via one of the channels below. Include enough
information to reproduce and assess impact:

- A clear description of the issue and the affected component / file
- Reproduction steps or a minimal proof-of-concept
- Impact assessment (what an attacker could achieve)
- Environment details if relevant (OS, runtime version)

### Private reporting channels

- **GitHub private vulnerability report:** use the
  *“Report a vulnerability”* button on the repository *Security* tab.
  This creates a private advisory visible only to maintainers.
- **Email:** security contact listed on the maintainer profile (no
  PGP requirement, but PGP-encrypted email is supported if offered).

You should receive an acknowledgement within **5 business days**.

## What to expect after reporting

1. Triage within 5 business days — we confirm receipt and assign a
   severity (Critical / High / Medium / Low).
2. A patch or workaround timeline is communicated within 10 business
   days for High / Critical issues.
3. Once a fix is shipped we publish a coordinated advisory on GitHub
   and credit the reporter (unless you ask to remain anonymous).
4. If we cannot reproduce or do not consider the report a security
   issue, we will explain why in a follow-up.

## Scope

In scope: vulnerabilities in this repository’s source code, default
configuration, CI workflows, and any documented deployment paths.

Out of scope:

- Vulnerabilities in upstream dependencies (please report upstream)
- Issues requiring physical / local-machine access only
- Social engineering or denial-of-service against the maintainer
- “Theoretical” findings without a concrete attack path

## Hardening references

See `HARDENING_NOTES.md` (if present) for design decisions relevant
to the security posture of this project.
