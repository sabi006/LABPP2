# db.py
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from config import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT


def connection_params(database=None):
    params = {
        "dbname": database or DB_NAME,
        "user": DB_USER,
        "host": DB_HOST,
        "port": DB_PORT,
    }
    if DB_PASSWORD:
        params["password"] = DB_PASSWORD
    return params


def ensure_database_exists():
    """Creates the database automatically if it does not exist."""
    try:
        conn = psycopg2.connect(**connection_params(DB_NAME))
        conn.close()
        return
    except psycopg2.OperationalError:
        pass

    admin_conn = psycopg2.connect(**connection_params("postgres"))
    admin_conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = admin_conn.cursor()
    cur.execute("SELECT 1 FROM pg_database WHERE datname = %s;", (DB_NAME,))
    exists = cur.fetchone()
    if not exists:
        cur.execute(f'CREATE DATABASE "{DB_NAME}";')
    cur.close()
    admin_conn.close()


def get_connection():
    return psycopg2.connect(**connection_params(DB_NAME))


def create_tables():
    ensure_database_exists()
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS players (
            id SERIAL PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS game_sessions (
            id SERIAL PRIMARY KEY,
            player_id INTEGER REFERENCES players(id) ON DELETE CASCADE,
            score INTEGER NOT NULL,
            level_reached INTEGER NOT NULL,
            played_at TIMESTAMP DEFAULT NOW()
        );
    """)

    conn.commit()
    cur.close()
    conn.close()


def get_or_create_player(username):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id FROM players WHERE username = %s;", (username,))
    row = cur.fetchone()
    if row:
        player_id = row[0]
    else:
        cur.execute("INSERT INTO players(username) VALUES (%s) RETURNING id;", (username,))
        player_id = cur.fetchone()[0]
        conn.commit()
    cur.close()
    conn.close()
    return player_id


def save_result(username, score, level_reached):
    player_id = get_or_create_player(username)
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO game_sessions(player_id, score, level_reached)
        VALUES (%s, %s, %s);
        """,
        (player_id, score, level_reached),
    )
    conn.commit()
    cur.close()
    conn.close()


def get_top_10():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT p.username, g.score, g.level_reached, g.played_at
        FROM game_sessions g
        JOIN players p ON g.player_id = p.id
        ORDER BY g.score DESC, g.level_reached DESC, g.played_at ASC
        LIMIT 10;
    """)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows


def get_personal_best(username):
    if not username:
        return 0
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT COALESCE(MAX(g.score), 0)
        FROM game_sessions g
        JOIN players p ON g.player_id = p.id
        WHERE p.username = %s;
    """, (username,))
    best = cur.fetchone()[0]
    cur.close()
    conn.close()
    return best
