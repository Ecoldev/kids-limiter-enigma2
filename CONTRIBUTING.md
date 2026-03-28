# Contributing

Thank you for your interest in contributing to KidsLimiter!

## How to contribute

You can contribute in several ways:

* reporting bugs
* suggesting new features
* improving documentation
* submitting pull requests

---

## Reporting issues

When creating an issue, please include:

* description of the problem
* steps to reproduce
* expected behavior
* logs (if available)

---

## Development setup

Clone the repository:

```bash
git clone https://github.com/Ecoldev/kids-limiter-enigma2.git
cd kids-limiter-enigma2
```

No special environment is required for basic development and testing.

---

## Running tests

Run tests locally:

```bash
python3 test_time.py
```

---

## Code style

* keep code simple and readable
* follow existing structure
* avoid unnecessary complexity
* use meaningful variable names

---

## Pull requests

Before submitting a PR:

* ensure code builds without errors
* run tests locally
* describe your changes clearly
* link related issues (e.g. `Fixes #11`)

---

## Branching

Recommended workflow:

* create a feature branch from `main`
* name it using issue number:

  * `11-fix-time-handling`
  * `1-add-pin-protection`

---

## Notes

* This project runs on Enigma2 (Python 2.7 environment)
* CI runs on Python 3.x for logic validation
* Always test runtime behavior on a real device

---

## Code of Conduct

By participating in this project, you agree to follow the Code of Conduct.
