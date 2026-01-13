# Secure CI/CD Pipeline Demo (DevSecOps)

![CI](../../actions/workflows/ci.yml/badge.svg)


A minimal FastAPI project with a CI/CD pipeline that includes automated testing and security gates.

## What the pipeline does
On every push / pull request:
- ✅ Runs unit/API tests (pytest)
- ✅ Scans for leaked secrets (Gitleaks)
- ✅ Scans dependencies/filesystem for HIGH/CRITICAL vulnerabilities (Trivy)
- ✅ Runs SAST static analysis (Semgrep)
- ❌ Fails the pipeline if any security gate finds issues

## Tech
- GitHub Actions
- FastAPI + pytest
- Gitleaks, Trivy, Semgrep
- Dependabot updates

  Open:
http://127.0.0.1:8000/health
http://127.0.0.1:8000/hello
http://127.0.0.1:8000/hello?name=blonde


## Run locally
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload


