import os
from dotenv import load_dotenv
import psycopg2

load_dotenv()

try:
    # Test direct connection
    conn = psycopg2.connect(os.getenv('DATABASE_URL'))
    print('✅ Direct PostgreSQL connection successful!')
    conn.close()
except Exception as e:
    print('❌ Direct connection failed:', str(e))
    print('Using SQLite fallback for development')