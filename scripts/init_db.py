#!/usr/bin/env python3
"""
Piper Morgan 1.0 - Database Initialization Script
Creates all required tables using SQLAlchemy models (domain-first architecture)
"""

import asyncio
import os

from dotenv import load_dotenv

# Load environment variables
load_dotenv()


async def init_database():
    """Initialize database using SQLAlchemy models"""
    from services.database.connection import db
    from services.database.models import Base

    print("🗄️  Initializing database connection...")
    await db.initialize()

    print("🗄️  Dropping existing tables to ensure clean schema...")
    async with db.engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    print("🗄️  Creating tables from SQLAlchemy models...")
    await db.create_tables()

    print("✅ Database schema initialized successfully from domain models!")


if __name__ == "__main__":
    asyncio.run(init_database())
