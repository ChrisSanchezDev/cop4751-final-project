import mysql.connector

DB_CONFIG = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'root',
    'password': '8JgyjD',
    'database': 'job_tracker'
}

def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)

def query_all(sql, params=None):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(sql, params or ())
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return results

def query_one(sql, params=None):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(sql, params or ())
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result

def execute_write(sql, params=None):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(sql, params or ())
    conn.commit()
    last_id = cursor.lastrowid
    cursor.close()
    conn.close()
    return last_id