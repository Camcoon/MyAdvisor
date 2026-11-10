"""Retain genuine correction-run output using fresh disposable databases/temp.

From the project root: .venv/Scripts/python.exe
docs/assignment2/run_correction_checks.py targeted|full|unit|integration|contrast
Browser checks need local Chromium/Node/pinned CSS and a working renderer.
Never initializes the normal application database or prints signing keys.
"""
import argparse
import hashlib
import json
import os
import sqlite3
import subprocess
import sys
import tempfile
import uuid
from datetime import datetime, timezone
from importlib.metadata import version
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "docs/assignment2/evidence/corrections-2026-10-27"


def source_hashes():
    return {
        str(p.relative_to(ROOT)).replace("\\", "/"): hashlib.sha256(p.read_bytes()).hexdigest()
        for folder in ("app", "tests")
        for p in sorted((ROOT / folder).rglob("*"))
        if p.is_file() and "__pycache__" not in p.parts
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("scope", choices=["targeted", "degree", "full", "unit", "integration", "contrast"])
    parser.add_argument("--evidence-dir", type=Path, default=OUT)
    args = parser.parse_args()
    selections = {
        "targeted": ["tests/integration", "tests/test_advising_service.py", "tests/test_api_security.py"],
        "degree": ["tests/unit/test_demo_requirements.py", "tests/integration/test_demo_requirement_migration.py",
                   "tests/test_advising_service.py"],
        "full": ["tests"], "unit": ["tests", "-m", "unit"],
        "integration": ["tests", "-m", "integration"],
        "contrast": ["tests/integration/test_contrast_regression.py", "-s"],
    }
    out = args.evidence_dir.resolve()
    out.mkdir(parents=True, exist_ok=True)
    started = datetime.now(timezone.utc)
    run_id = args.scope + "-" + started.strftime("%Y%m%dT%H%M%SZ") + "-" + uuid.uuid4().hex[:8]
    temporary = Path(tempfile.mkdtemp(prefix="MyAdvisor-A2-Corrections-"))
    bootstrap = temporary / "unused-bootstrap.db"
    env = os.environ.copy()
    env.update({
        "DATABASE_URI": "sqlite:///" + bootstrap.as_posix(),
        "ENV": "audit-corrections",
        "SECRET_KEY": uuid.uuid4().hex + uuid.uuid4().hex,
        "PYTHONDONTWRITEBYTECODE": "1",
    })
    command = [sys.executable, "-m", "pytest", *selections[args.scope], "-q",
               "-p", "no:cacheprovider", "--basetemp=" + str(temporary / "pytest-base"),
               "--junitxml=" + str(out / (run_id + ".xml"))]
    before = source_hashes()
    result = subprocess.run(command, cwd=ROOT, env=env, capture_output=True, text=True,
                            encoding="utf-8", errors="replace", check=False)
    (out / (run_id + ".txt")).write_text(result.stdout + result.stderr, encoding="utf-8")
    after = source_hashes()
    metadata = {
        "run_id": run_id, "scope": args.scope, "command": command,
        "started_utc": started.isoformat(), "finished_utc": datetime.now(timezone.utc).isoformat(),
        "exit_code": result.returncode, "python": sys.version,
        "versions": {name: version(name) for name in ["pytest", "fastapi", "sqlmodel", "SQLAlchemy", "PyJWT", "pwdlib"]},
        "sqlite": sqlite3.sqlite_version, "temporary_directory": str(temporary),
        "bootstrap_database_created": bootstrap.exists(),
        "source_sha256": before, "source_unchanged_during_run": before == after,
        "pdf_sha256": (hashlib.sha256((ROOT / "docs/assignment2/COMP3613_Assignment2_MyAdvisor.pdf").read_bytes()).hexdigest()
                       if (ROOT / "docs/assignment2/COMP3613_Assignment2_MyAdvisor.pdf").is_file() else None),
        "postman_collection_sha256": hashlib.sha256((ROOT / "docs/assignment2/postman/MyAdvisor-Assignment2.postman_collection.json").read_bytes()).hexdigest(),
        "environment_scope": "Generated process-local signing key (not retained); isolated fixture DBs; no normal/deployed DB initialized",
    }
    (out / (run_id + ".json")).write_text(json.dumps(metadata, indent=2), encoding="utf-8")
    print(result.stdout[-4500:])
    print("Run record:", run_id, "Exit:", result.returncode)
    if bootstrap.exists() or before != after:
        raise SystemExit("Isolation/source invariant failed; inspect run metadata")
    raise SystemExit(result.returncode)


if __name__ == "__main__":
    main()
