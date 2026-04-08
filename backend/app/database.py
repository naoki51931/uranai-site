from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.config import get_settings
settings = get_settings()

engine = create_engine(settings.database_url, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def ensure_runtime_schema() -> None:
    # The project does not use migrations yet, so runtime-safe column adds keep
    # existing environments compatible when new learning features are introduced.
    with engine.begin() as conn:
        if engine.dialect.name == "mysql":
            existing_columns = {
                row[0]
                for row in conn.exec_driver_sql(
                    """
                    SELECT COLUMN_NAME
                    FROM information_schema.COLUMNS
                    WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'tarot_readings'
                    """
                )
            }
            if "strategy_version" not in existing_columns:
                conn.exec_driver_sql(
                    """
                    ALTER TABLE tarot_readings
                    ADD COLUMN strategy_version VARCHAR(64) NOT NULL DEFAULT 'baseline-v1'
                    """
                )
            if "learning_context" not in existing_columns:
                conn.exec_driver_sql(
                    """
                    ALTER TABLE tarot_readings
                    ADD COLUMN learning_context TEXT NULL
                    """
                )
            if "premium_explanations_json" not in existing_columns:
                conn.exec_driver_sql(
                    """
                    ALTER TABLE tarot_readings
                    ADD COLUMN premium_explanations_json TEXT NULL
                    """
                )


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
