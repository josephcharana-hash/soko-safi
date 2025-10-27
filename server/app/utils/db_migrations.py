from sqlalchemy import inspect, text
from app.models import db


def ensure_deleted_at_columns(app):
    """Ensure `deleted_at` column exists on categories and subcategories tables.
    This performs a simple ALTER TABLE ADD COLUMN when using SQLite. For other
    dialects this function logs a message recommending a migration.

    NOTE: this function expects to be called while the Flask app context is active
    (the calling code should enter app.app_context()).
    """
    # Use the SQLAlchemy engine attached to the db instance (app context required)
    engine = db.engine
    insp = inspect(engine)

    tables = [
        ("categories", "deleted_at"),
        ("subcategories", "deleted_at"),
    ]

    for table_name, col in tables:
        if not insp.has_table(table_name):
            continue
        columns = [c["name"] for c in insp.get_columns(table_name)]
        if col in columns:
            continue

        # Add column for SQLite (simple, nullable)
        if engine.dialect.name == "sqlite":
            sql = f"ALTER TABLE {table_name} ADD COLUMN {col} DATETIME"
            try:
                with engine.connect() as conn:
                    conn.execute(text(sql))
                    conn.commit()
                print(f"Added column {col} to {table_name}")
            except Exception as e:
                print(f"Failed to add column {col} to {table_name}: {e}")
        else:
            # For other DBs, log and skip - migrations required
            print(f"Column {col} missing on {table_name}. Please run a DB migration for {engine.dialect.name}.")
