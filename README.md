# Secure CI/CD Pipeline Demo (DevSecOps)

![CI](../../actions/workflows/ci.yml/badge.svg)


A minimal FastAPI project with a CI/CD pipeline that includes automated testing and security gates.

## What the pipeline does
On every push / pull request:
- ✅ Runs unit/API tests (pytest)
- ✅ Scans for leaked secrets (Gitleaks)
- ✅ Scans dependencies/filesystem for HIGH/CRITICAL vulnerabilities (Trivy)
- ✅ Runs SAST static analysis (Semgrep)
- 🚫 Automatically blocks the pipeline if any security gate finds issues


## Tech
- GitHub Actions
- FastAPI + pytest
- Gitleaks, Trivy, Semgrep
- Dependabot updates


## Controlled failure demo (how to make CI fail on purpose)

This repo includes a policy-driven CI pipeline. To demonstrate enforcement, you can intentionally trigger failures:

### 1) Fail the pipeline via tests
Edit any test expectation (for example change `"hello, world"` to `"hello, blonde"`) and push the commit.
    
The **Run tests** step will fail with an AssertionError.

### 2) Fail the pipeline via secrets gate (safe demo)
Create a temporary file `demo_secret.txt` with a fake secret-like string, commit, and push:AWS_SECRET_ACCESS_KEY=****random_fake_key****    

The secrets scan will report a finding, and the **Policy Gate** will block the pipeline.





## Run locally
```bash

cd ~
git clone https://github.com/lastet/secure-cicd-pipeline-demo.git


cd secure-cicd-pipeline-demo
ls


python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload


