import asyncio
import os
import sys

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.sql import text

# Add project root to path to allow imports
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from services.database.connection import db


async def main():
    """
    Connects to the database and adds the 'created_at' column
    to the 'tasks' table if it doesn't already exist.
    """
    print("Connecting to the database to perform migration...")

    # Load env from project root and get DB URL
    dotenv_path = os.path.join(project_root, ".env")
    load_dotenv(dotenv_path=dotenv_path)

    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        print(
            f"❌ DATABASE_URL not set in environment. Looked for .env at: {dotenv_path}"
        )
        return

    # Use the existing db object for connection URL
    engine = create_async_engine(db_url)

    async with engine.connect() as conn:
        try:
            # Check if the column exists
            check_column_query = text(
                """
                SELECT 1
                FROM information_schema.columns
                WHERE table_schema = 'public'
                  AND table_name = 'tasks'
                  AND column_name = 'created_at';
            """
            )
            result = await conn.execute(check_column_query)
            column_exists = result.scalar_one_or_none()

            if column_exists:
                print(
                    "✅ Column 'created_at' already exists in 'tasks' table. No action needed."
                )
                return

            # If column does not exist, add it
            print("Column 'created_at' not found. Adding it to the 'tasks' table...")

            # The connection is already in a transaction, so we don't need conn.begin()

            # Add the column with a default value.
            # For existing rows, this will be set to the time the command is run.
            # For new rows, SQLAlchemy's default will take precedence.
            alter_table_query = text(
                """
                ALTER TABLE tasks ADD COLUMN created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT now();
            """
            )
            await conn.execute(alter_table_query)

            await conn.commit()

            print("✅ Successfully added 'created_at' column to 'tasks' table.")

        except Exception as e:
            print(f"❌ An error occurred during migration: {e}")
            await conn.rollback()
        finally:
            await conn.close()


if __name__ == "__main__":
    print("--- Running Database Migration for Task.created_at ---")
    asyncio.run(main())
    print("--- Migration script finished ---")
