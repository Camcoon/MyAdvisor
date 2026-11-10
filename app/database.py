import logging
import threading
import time
from contextlib import contextmanager

from sqlalchemy import event, inspect, text
from sqlalchemy.engine import Engine
from sqlalchemy.exc import DBAPIError, OperationalError, ProgrammingError
from sqlmodel import Session, SQLModel, create_engine

from app.config import get_settings

logger = logging.getLogger(__name__)

_schema_lock = threading.Lock()


def sqlalchemy_uri(uri: str) -> str:
    """Accept Render's postgres:// URLs in the sync SQLAlchemy engine."""
    if uri.startswith("postgres://"):
        return "postgresql+psycopg2://" + uri[len("postgres://") :]
    if uri.startswith("postgresql://"):
        return "postgresql+psycopg2://" + uri[len("postgresql://") :]
    return uri


def _enable_sqlite_foreign_keys(dbapi_connection, _connection_record) -> None:
    # Python 3.12+ may use autocommit=False. SQLite ignores this PRAGMA inside
    # a transaction, so temporarily enable autocommit and restore the policy.
    has_autocommit = hasattr(dbapi_connection, "autocommit")
    previous_autocommit = getattr(dbapi_connection, "autocommit", None)
    if has_autocommit:
        dbapi_connection.autocommit = True
    try:
        cursor = dbapi_connection.cursor()
        try:
            cursor.execute("PRAGMA foreign_keys=ON")
        finally:
            cursor.close()
    finally:
        if has_autocommit:
            dbapi_connection.autocommit = previous_autocommit


def create_app_engine(uri: str, **kwargs) -> Engine:
    """Apply runtime connection policy to the application's own engines only."""
    app_engine = create_engine(sqlalchemy_uri(uri), **kwargs)
    if app_engine.dialect.name == "sqlite":
        event.listen(app_engine, "connect", _enable_sqlite_foreign_keys)
    return app_engine


engine = create_app_engine(
    sqlalchemy_uri(get_settings().database_uri),
    echo=get_settings().env.lower()
    in ["dev", "development", "test", "testing", "staging"],
    pool_size=get_settings().db_pool_size,
    max_overflow=get_settings().db_additional_overflow,
    pool_timeout=get_settings().db_pool_timeout,
    pool_recycle=get_settings().db_pool_recycle,
)


def create_db_and_tables() -> None:
    # Ensure model modules are imported so tables are registered on metadata.
    import app.models  # noqa: F401

    SQLModel.metadata.create_all(engine)
    upgrade_existing_schema(engine)


def upgrade_existing_schema(bind: Engine) -> None:
    """Add the new MyAdvisor fields to databases created from the earlier MVP."""
    column_additions = {
        "user": {
            "name": "VARCHAR NOT NULL DEFAULT ''",
            "student_number": "VARCHAR",
            "degree_program": "INTEGER REFERENCES degreeprogram (id)",
        },
        "course": {
            "department": "VARCHAR NOT NULL DEFAULT 'Computer Science'",
        },
        "semesterplan": {
            "submitted_at": "DATETIME",
        },
        "studentcourse": {
            "completed_at": "DATETIME",
        },
    }

    with bind.begin() as connection:
        inspector = inspect(connection)
        existing_tables = set(inspector.get_table_names())
        for table_name, additions in column_additions.items():
            if table_name not in existing_tables:
                continue
            columns = {column["name"] for column in inspector.get_columns(table_name)}
            for column_name, definition in additions.items():
                if column_name not in columns:
                    connection.exec_driver_sql(
                        f'ALTER TABLE "{table_name}" '
                        f'ADD COLUMN "{column_name}" {definition}'
                    )

        if "semesterplan" in existing_tables:
            connection.execute(
                text(
                    "UPDATE semesterplan SET submitted_at = CURRENT_TIMESTAMP "
                    "WHERE submitted_at IS NULL"
                )
            )

        unique_pairs = (
            ("studentcourse", ("student_id", "course_id"), "uq_studentcourse_student_course"),
            ("plancourse", ("plan_id", "course_id"), "uq_plancourse_plan_course"),
            ("degreerequirement", ("program_id", "category"), "uq_requirement_program_category"),
        )
        for table_name, column_names, index_name in unique_pairs:
            if table_name not in existing_tables:
                continue
            unique_constraints = {
                tuple(constraint["column_names"])
                for constraint in inspector.get_unique_constraints(table_name)
            }
            unique_indexes = {
                tuple(index["column_names"])
                for index in inspector.get_indexes(table_name)
                if index["unique"]
            }
            if column_names not in unique_constraints | unique_indexes:
                columns_sql = ", ".join(f'"{column}"' for column in column_names)
                connection.exec_driver_sql(
                    f'CREATE UNIQUE INDEX IF NOT EXISTS "{index_name}" '
                    f'ON "{table_name}" ({columns_sql})'
                )

        if "user" in existing_tables:
            user_unique_constraints = {
                tuple(constraint["column_names"])
                for constraint in inspector.get_unique_constraints("user")
            }
            user_unique_indexes = {
                tuple(index["column_names"])
                for index in inspector.get_indexes("user")
                if index["unique"]
            }
            if ("student_number",) not in user_unique_constraints | user_unique_indexes:
                connection.exec_driver_sql(
                    "CREATE UNIQUE INDEX IF NOT EXISTS "
                    '"uq_user_student_number" ON "user" ("student_number")'
                )
            connection.exec_driver_sql(
                "CREATE INDEX IF NOT EXISTS "
                '"ix_user_degree_program" ON "user" ("degree_program")'
            )


def drop_all() -> None:
    SQLModel.metadata.drop_all(bind=engine)


def is_db_not_ready_error(exc: BaseException) -> bool:
    """True when Postgres is unreachable or the schema/tables are missing."""
    if isinstance(exc, OperationalError):
        return True
    if isinstance(exc, ProgrammingError):
        return True
    if isinstance(exc, DBAPIError) and getattr(exc, "connection_invalidated", False):
        return True

    text = str(exc).lower()
    markers = (
        "does not exist",
        "undefinedtable",
        "undefined table",
        "no such table",
        "relation ",
        "could not connect",
        "connection refused",
        "connection timed out",
        "server closed the connection",
        "the database system is starting up",
        "remaining connection slots",
        "too many connections",
        "ssl connection has been closed",
    )
    return any(m in text for m in markers)


def ensure_db_and_tables(
    *,
    retries: int = 8,
    delay_seconds: float = 2.0,
) -> None:
    """Create tables, retrying while the prod DB is still coming up."""
    last: BaseException | None = None
    for attempt in range(1, retries + 1):
        try:
            with _schema_lock:
                create_db_and_tables()
            if attempt > 1:
                logger.info("Database schema ready after %s attempt(s)", attempt)
            return
        except Exception as exc:
            last = exc
            if not is_db_not_ready_error(exc) or attempt >= retries:
                raise
            logger.warning(
                "Database not ready (attempt %s/%s): %s",
                attempt,
                retries,
                exc,
            )
            time.sleep(delay_seconds * attempt)
    if last is not None:
        raise last


def recover_if_uninitialized(exc: BaseException) -> bool:
    """If *exc* looks like a missing schema, create tables and return True."""
    if not is_db_not_ready_error(exc):
        return False
    logger.warning("Uninitialized database detected; creating tables: %s", exc)
    ensure_db_and_tables()
    return True


def _session_generator():
    with Session(engine) as session:
        try:
            yield session
        except Exception as e:
            logger.error(f"Database session error: {e}")
            raise
        finally:
            session.close()


def get_session():
    yield from _session_generator()


@contextmanager
def get_cli_session():
    yield from _session_generator()
