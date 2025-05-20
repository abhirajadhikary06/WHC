import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
import os
from datetime import datetime
import pytz

DATABSE_URL = "postgresql://neondb_owner:npg_jeo6KPxV4UED@ep-silent-poetry-a1ujigrh-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require"

def get_db_connection():
    try:
        conn = psycopg2.connect(os.getenv('DATABASE_URL'))
        return conn
    except Exception as e:
        print(f"Database connection error: {e}")
        raise

def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS website_checks_log (
            id SERIAL PRIMARY KEY,
            url TEXT NOT NULL,
            status_code INTEGER,
            status_message VARCHAR(100),
            response_time_ms NUMERIC(10, 2),
            checked_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
            error_message TEXT
        );
    """)
    conn.commit()
    cur.close()
    conn.close()

def fetch_recent_checks(limit=10):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT id, url, status_code, status_message, response_time_ms, checked_at, error_message FROM website_checks_log ORDER BY checked_at DESC LIMIT %s", (limit,))
    checks = cur.fetchall()
    # Convert checked_at to IST and format as "YYYY-MM-DD HH:MM:SS"
    ist = pytz.timezone('Asia/Kolkata')
    for check in checks:
        if check['checked_at']:
            check['checked_at'] = check['checked_at'].astimezone(ist).strftime('%Y-%m-%d %H:%M:%S')
    cur.close()
    conn.close()
    return checks

if __name__ == '__main__':
    init_db()