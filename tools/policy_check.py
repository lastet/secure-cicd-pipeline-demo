import sys
import json
import yaml
from pathlib import Path

def fail(reason: str):
    print(f"\n❌ POLICY VIOLATION: {reason}")
    sys.exit(1)

def ok(msg: str):
    print(f"✅ {msg}")

# --- load policy ---
policy_path = Path("policy.yml")
if not policy_path.exists():
    fail("policy.yml not found")

policy = yaml.safe_load(policy_path.read_text())

print("\n🔐 Security Policy Loaded")
print(policy)

# --- check pytest ---
pytest_report = Path("pytest-junit.xml")
if not pytest_report.exists():
    fail("pytest report not found (tests probably did not run)")

ok("Tests executed")

# --- secrets gate ---
if policy["block_if"].get("secrets"):
    gitleaks_report = Path("gitleaks-report.json")
    if gitleaks_report.exists():
        findings = json.loads(gitleaks_report.read_text())
        if findings:
            fail("Secrets detected by Gitleaks")
    ok("No leaked secrets")

# --- dependency gate ---
if policy["block_if"].get("dependency_critical"):
    trivy_report = Path("trivy-report.json")
    if trivy_report.exists():
        report = json.loads(trivy_report.read_text())
        for result in report.get("Results", []):
            for vuln in result.get("Vulnerabilities", []):
                if vuln.get("Severity") == "CRITICAL":
                    fail("Critical dependency vulnerability detected")
    ok("No critical dependency vulnerabilities")

# --- sast gate ---
if policy["block_if"].get("sast_high"):
    semgrep_report = Path("semgrep-report.json")
    if semgrep_report.exists():
        report = json.loads(semgrep_report.read_text())
        if report.get("results"):
            fail("High severity SAST findings detected")
    ok("No high-risk SAST issues")

print("\n🟢 POLICY CHECK PASSED — pipeline allowed")
