"""Backed-up, explicit SQLite migration of approved fictional requirements only."""

import hashlib
import json
import sqlite3
import uuid
from datetime import datetime, timezone
from pathlib import Path

from sqlalchemy.engine import make_url
from sqlmodel import SQLModel


def backup_sqlite_database(database_uri: str, directory: Path) -> Path:
    """Use SQLite's online backup API, including committed WAL data; never reset."""
    url = make_url(database_uri)
    if url.get_backend_name() != "sqlite" or not url.database or url.database == ":memory:":
        raise ValueError("Apply requires an existing SQLite file; other databases need a reviewed snapshot migration.")
    source = Path(url.database).resolve()
    if not source.is_file():
        raise ValueError("Existing SQLite database file not found; refusing to create or initialize it.")
    directory.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    target = directory / f"{source.stem}-before-degree-93-{stamp}-{uuid.uuid4().hex[:8]}.sqlite3"
    with target.open("xb"):
        pass
    with (sqlite3.connect(source.as_uri() + "?mode=ro", uri=True) as original,
          sqlite3.connect(target) as backup):
        original.backup(backup)
        if backup.execute("PRAGMA integrity_check").fetchone()[0] != "ok":
            raise ValueError("Backup integrity check failed; migration was not applied.")
    return target


def table_fingerprints(session) -> dict:
    """Retain counts/digests, never personal row contents or credentials."""
    result = {}
    for table in SQLModel.metadata.sorted_tables:
        rows = session.execute(table.select().order_by(*table.primary_key.columns)).mappings().all()
        payload = json.dumps([dict(row) for row in rows], sort_keys=True, default=str).encode()
        result[table.name] = {"rows": len(rows), "sha256": hashlib.sha256(payload).hexdigest()}
    return result


def migrate_demo_requirements(session, database_uri: str, backup_directory: Path, *, apply: bool) -> dict:
    from app.services.advising_service import AdvisingService

    service = AdvisingService(session)
    review = service.sync_demo_requirements()
    result = {"allocation": review, "applied": False, "backup": None}
    if not apply or not any(item["changed"] for item in review):
        return result
    before = table_fingerprints(session)
    session.rollback()  # Release the read transaction before backing up.
    backup = backup_sqlite_database(database_uri, backup_directory)
    service.sync_demo_requirements(apply=True)
    after = table_fingerprints(session)
    unchanged = all(before[name] == after[name] for name in before if name != "degreerequirement")
    result.update(applied=True, backup=str(backup), before=before, after=after,
                  other_tables_unchanged=unchanged)
    if not unchanged or any(item["changed"] for item in service.sync_demo_requirements()):
        raise RuntimeError(f"Post-migration verification failed; retain backup at {backup} and investigate.")
    return result
