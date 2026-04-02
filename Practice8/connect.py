import psycopg2

DB_CONFIG = {
    "host": "localhost",
    "database": "phonebook_db",
    "user": "postgres",
    "password": "23455432",
    "port": 5432  
}

def connect():
    try:
        conn = psycopg2.connect(
            host=DB_CONFIG["host"],
            database=DB_CONFIG["database"],
            user=DB_CONFIG["user"],
            password=DB_CONFIG["password"],
            port=DB_CONFIG["port"]
        )
        print("Connected successfully")
        return conn
    except Exception as e:
        print("Connection error:", e)
        return None