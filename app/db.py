# app/db.py
import json
import os
import asyncpg

DB_USER = os.getenv("APP_DB_USER", "postgres")
DB_PASSWORD = os.getenv("APP_DB_PASSWORD", "postgres")
DB_NAME = os.getenv("APP_DB_NAME", "lxc_db")
DB_HOST = os.getenv("APP_DB_HOST", "db")
DB_PORT = int(os.getenv("APP_DB_PORT", "5432"))


async def get_connection():
    return await asyncpg.connect(
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        host=DB_HOST,
        port=DB_PORT,
    )


async def init_db(conn):
    await conn.execute(
        """
        CREATE TABLE IF NOT EXISTS lxc_containers (
            id SERIAL PRIMARY KEY,
            name TEXT,
            cpu_usage BIGINT,
            memory_usage BIGINT,
            created_at BIGINT,
            status TEXT,
            ip_addresses JSONB NOT NULL
        );
        """
    )


async def insert_containers(conn, containers):
    if not containers:
        return

    await conn.executemany(
        """
        INSERT INTO lxc_containers (
            name, cpu_usage, memory_usage, created_at, status, ip_addresses
        ) VALUES ($1, $2, $3, $4, $5, $6);
        """,
        [
            (
                c["name"],
                c["cpu_usage"],
                c["memory_usage"],
                c["created_at"],
                c["status"],
                json.dumps(c["ip_addresses"])
            )
            for c in containers
        ],
    )
