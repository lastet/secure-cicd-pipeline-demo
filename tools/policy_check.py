import sys
import yaml
import json
from pathlib import Path

POLICY_FILE = "policy.yml"

# ---------- Load policy ----------
def load_policy():
    if not Path(POLICY_FILE).exists():
        print(f"[POLICY] {POLICY_FILE} not found -> ALLOW")
        return {}
    return yaml.safe_load(Path(POLICY_FILE).read_text()) or {}

# ---------- Gitleaks ----------
def gitleaks_findings_count():
    sarif_path = Path("results.sarif")

    if not sarif_path.exists():
        print("[POLICY] results.sarif not found -> assume 0 findings")
        return 0

    data = json.loads(sarif_path.read_text(encoding="utf-8"))
    runs = data.get("runs", [])
    total = sum(len(run.get("results", [])) for run in runs)

    print(f"[POLICY] gitleaks findings (SARIF): {total}")
    return total

# ---------- Main ----------
def main():
    policy = load_policy()
    block_if = policy.get("block_if", {})

    secrets_block = bool(block_if.get("secrets", False))
    findings = gitleaks_findings_count()

    print(f"[POLICY] secrets_block={secrets_block}, gitleaks_findings={findings}")

    if secrets_block and findings > 0:
        print("[POLICY] ❌ BLOCK: secrets detected")
        sys.exit(1)

    print("[POLICY] ✅ ALLOW: policy satisfied")
    sys.exit(0)

if __name__ == "__main__":
    main()
