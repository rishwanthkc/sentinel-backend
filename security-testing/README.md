# Sentinel Backend Security Testing

This folder contains security assessment tooling and generated artifacts for the backend only.

## Files

- `auto_vuln.txt` — security testing specification.
- `documentation/` — endpoint discovery and summary docs.
- `reports/` — generated JSON, Excel, and PDF reports.
- `scripts/generate_security_artifacts.py` — static report generation from source discovery.
- `scripts/security_test_runner.py` — runtime DAST harness using `input.json`.
- `input.json` — runtime configuration template.

## How to run

1. Activate the backend virtual environment.
2. Ensure `security-testing/input.json` is populated with `baseUrl` and role tokens.
3. Run the runtime assessment:

```powershell
cd sentinel-backend
c:/Users/rishi/OneDrive/Desktop/SENTINEL/.venv/Scripts/python.exe security-testing/scripts/security_test_runner.py
```

4. Generated reports appear in `security-testing/reports/`.

## Notes

- Only safe HTTP methods are used.
- No external domains are tested.
- The harness only runs if `input.json` exists and `baseUrl` is provided.
