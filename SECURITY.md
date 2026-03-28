# Security Policy

## Supported Versions

Currently supported versions:

* v0.1 (latest)

Only the latest version is actively maintained and receives security updates.

---

## Reporting a Vulnerability

If you discover a security vulnerability, please report it responsibly.

### Please include:

* description of the issue
* steps to reproduce
* potential impact
* suggested fix (if possible)

### How to report

* Open a GitHub issue (for non-sensitive issues)
* For sensitive vulnerabilities, contact the maintainer directly

---

## Scope

This project is an Enigma2 plugin and handles:

* local file storage (`/etc/enigma2/kids_time.json`)
* user interaction via Enigma2 UI

No external network communication is performed by default.

---

## Known limitations

* No PIN protection (planned in future versions)
* Local file can be modified manually
* No encryption of stored data

---

## Best practices for users

* restrict access to the device (SSH / root access)
* avoid exposing Enigma2 interface publicly
* keep your system up to date

---

## Disclaimer

This project is provided "as is" without warranty of any kind.

Use at your own risk.
