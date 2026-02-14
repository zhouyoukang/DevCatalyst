# Starter Prompt

Copy and paste the following into Windsurf Cascade:

---

Please read `{path-to-DevCatalyst}/installer/INSTALLER.md` and execute the full DevCatalyst v5.0 installation. Deploy both Layer 1 (global) and Layer 2 (project). Do not interrupt or ask questions. Output a configuration report when done.

---

> **Notes**:
> - Replace `{path-to-DevCatalyst}` with the actual path
> - If Layer 1 was previously deployed, AI will skip existing configs
> - All steps are idempotent (safe to re-run)
> - After deployment, run `/health-check` to verify
