import psycopg2
import environ
import os

# Load DATABASE_URL
env = environ.Env()
environ.Env.read_env(os.path.join(os.path.dirname(__file__), '.env'))
database_url = env('DATABASE_URL')

try:
    # Connect to database
    conn = psycopg2.connect(database_url)
    print("Connection successful!")
    # Optional: Check PostgreSQL version
    with conn.cursor() as cur:
        cur.execute("SELECT version();")
        version = cur.fetchone()
        print(f"PostgreSQL version: {version[0]}")
    conn.close()
except Exception as e:
    print(f"Connection failed: {e}")