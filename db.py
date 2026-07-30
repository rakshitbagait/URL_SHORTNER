from sqlalchemy import create_engine, text
from sqlalchemy.orm import declarative_base, sessionmaker

# PostgreSQL Credentials
DB_USER = "postgres"
DB_PASSWORD = "12345678"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "url_shortener_db"

# Connection to the default postgres database
DEFAULT_DB_URL = (
    f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/postgres"
)

# Connection to your project database
DATABASE_URL = (
    f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)


def create_database():
    """
    Create the database if it doesn't already exist.
    """
    engine = create_engine(DEFAULT_DB_URL, isolation_level="AUTOCOMMIT")

    with engine.connect() as conn:
        result = conn.execute(
            text(
                "SELECT 1 FROM pg_database WHERE datname=:dbname"
            ),
            {"dbname": DB_NAME},
        )

        if not result.scalar():
            conn.execute(text(f'CREATE DATABASE "{DB_NAME}"'))
            print(f"Database '{DB_NAME}' created successfully.")
        else:
            print(f"Database '{DB_NAME}' already exists.")

    engine.dispose()


# Create database if needed
create_database()

# Connect to your application database
engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()