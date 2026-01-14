import json
import os
import sys
import yaml

POLICY_FILE = "policy.yml"
GITLEAKS_REPORT = "gitleaks-report.json"

def load_policy():
    if not os.path.exists(POLICY_FILE):
        print(f"[POLICY] {POLICY_FILE} not found -> ALLOW")
        return {}
    with open(POLICY_FILE, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}

def gitleaks_findings_count():
    if not os.path.exists(GITLEAKS_REPORT):
        print(f"[POLICY] {GITLEAKS_REPORT} not found -> assume 0 findings")
        return 0

    raw = open(GITLEAKS_REPORT, "r", encoding="utf-8").read().strip()
    if not raw:
        print(f"[POLICY] {GITLEAKS_REPORT} empty -> 0 findings")
        return 0

    data = json.loads(raw)

    # Most common format from gitleaks: list of findings
    if isinstance(data, list):
        return len(data)

    # Fallback if the action wraps it in an object
    if isinstance(data, dict):
        for key in ("Leaks", "leaks", "findings", "Findings"):
            v = data.get(key)
            if isinstance(v, list):
                return len(v)

    return 0

def main():
    policy = load_policy()
    block_if = (policy.get("block_if") or {})

    secrets_block = bool(block_if.get("secrets", False))
    findings = gitleaks_findings_count()

    print(f"[POLICY] secrets_block={secrets_block}, gitleaks_findings={findings}")

    if secrets_block and findings > 0:
        print("[POLICY] BLOCK: secrets detected by Gitleaks")
        sys.exit(1)

    print("[POLICY] ALLOW: policy satisfied")
    sys.exit(0)

if __name__ == "__main__":
    main()
