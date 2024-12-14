import psycopg2

def save_to_database(data, table):
    conn = psycopg2.connect(
        host="localhost",
        port=5432,
        user="admin",
        password="password",
        dbname="hamf_db"
    )
    cur = conn.cursor()
    # Example insert
    cur.execute(f"INSERT INTO {table} (data) VALUES (%s)", (data,))
    conn.commit()
    conn.close()
