import os
import sqlite3
from pathlib import Path
from typing import Any, Dict, List

import psycopg
from psycopg.rows import dict_row

DATABASE_URL = os.getenv("DATABASE_URL", "")
USE_POSTGRES = DATABASE_URL.startswith("postgres://") or DATABASE_URL.startswith("postgresql://")
DB_PATH = Path(__file__).resolve().parent / "ledgerguard.db"


def get_sqlite_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def get_postgres_connection():
    return psycopg.connect(DATABASE_URL, row_factory=dict_row)


def get_connection():
    return get_postgres_connection() if USE_POSTGRES else get_sqlite_connection()


def placeholders(count: int):
    token = "%s" if USE_POSTGRES else "?"
    return ", ".join([token] * count)


def bind_token():
    return "%s" if USE_POSTGRES else "?"


def init_db():
    conn = get_connection()
    cur = conn.cursor()
    audit_id = "SERIAL PRIMARY KEY" if USE_POSTGRES else "INTEGER PRIMARY KEY AUTOINCREMENT"
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS invoice_results (
            invoice_id TEXT PRIMARY KEY,
            vendor TEXT NOT NULL,
            amount REAL NOT NULL,
            risk TEXT NOT NULL,
            risk_score INTEGER NOT NULL,
            reasons TEXT NOT NULL,
            recommendation TEXT NOT NULL,
            requires_human_approval INTEGER NOT NULL,
            approval_status TEXT NOT NULL,
            analyzed_at TEXT NOT NULL
        )
        """
    )
    cur.execute(
        f"""
        CREATE TABLE IF NOT EXISTS audit_log (
            id {audit_id},
            event TEXT NOT NULL,
            invoice_id TEXT,
            payload TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
        """
    )
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS approvals (
            invoice_id TEXT PRIMARY KEY,
            status TEXT NOT NULL,
            user_name TEXT NOT NULL,
            comment TEXT,
            timestamp TEXT NOT NULL
        )
        """
    )
    conn.commit()
    conn.close()


def upsert_invoice_result(result: Dict[str, Any]):
    conn = get_connection()
    sql = """
        INSERT INTO invoice_results (
            invoice_id, vendor, amount, risk, risk_score, reasons,
            recommendation, requires_human_approval, approval_status, analyzed_at
        ) VALUES ({values})
        ON CONFLICT(invoice_id) DO UPDATE SET
            vendor=excluded.vendor,
            amount=excluded.amount,
            risk=excluded.risk,
            risk_score=excluded.risk_score,
            reasons=excluded.reasons,
            recommendation=excluded.recommendation,
            requires_human_approval=excluded.requires_human_approval,
            approval_status=excluded.approval_status,
            analyzed_at=excluded.analyzed_at
    """.format(values=placeholders(10))
    conn.execute(
        sql,
        (
            result["invoice_id"],
            result["vendor"],
            result["amount"],
            result["risk"],
            result["risk_score"],
            ",".join(result["reasons"]),
            result["recommendation"],
            int(result["requires_human_approval"]),
            result["approval_status"],
            result["analyzed_at"],
        ),
    )
    conn.commit()
    conn.close()


def list_invoice_results() -> List[Dict[str, Any]]:
    conn = get_connection()
    rows = conn.execute("SELECT * FROM invoice_results").fetchall()
    conn.close()
    results = []
    for row in rows:
        item = dict(row)
        item["reasons"] = item["reasons"].split(",") if item["reasons"] else []
        item["requires_human_approval"] = bool(item["requires_human_approval"])
        results.append(item)
    return results


def get_invoice_result(invoice_id: str):
    conn = get_connection()
    sql = f"SELECT * FROM invoice_results WHERE invoice_id = {bind_token()}"
    row = conn.execute(sql, (invoice_id,)).fetchone()
    conn.close()
    if not row:
        return None
    item = dict(row)
    item["reasons"] = item["reasons"].split(",") if item["reasons"] else []
    item["requires_human_approval"] = bool(item["requires_human_approval"])
    return item


def insert_audit_event(event: str, invoice_id: str, payload: str, created_at: str):
    conn = get_connection()
    sql = "INSERT INTO audit_log (event, invoice_id, payload, created_at) VALUES ({values})".format(
        values=placeholders(4)
    )
    conn.execute(sql, (event, invoice_id, payload, created_at))
    conn.commit()
    conn.close()


def list_audit_events() -> List[Dict[str, Any]]:
    conn = get_connection()
    rows = conn.execute("SELECT * FROM audit_log ORDER BY id DESC").fetchall()
    conn.close()
    return [dict(row) for row in rows]


def upsert_approval(invoice_id: str, status: str, user: str, comment: str, timestamp: str):
    conn = get_connection()
    sql = """
        INSERT INTO approvals (invoice_id, status, user_name, comment, timestamp)
        VALUES ({values})
        ON CONFLICT(invoice_id) DO UPDATE SET
            status=excluded.status,
            user_name=excluded.user_name,
            comment=excluded.comment,
            timestamp=excluded.timestamp
    """.format(values=placeholders(5))
    conn.execute(sql, (invoice_id, status, user, comment, timestamp))
    update_sql = (
        f"UPDATE invoice_results SET approval_status = {bind_token()} "
        f"WHERE invoice_id = {bind_token()}"
    )
    conn.execute(update_sql, (status, invoice_id))
    conn.commit()
    conn.close()
