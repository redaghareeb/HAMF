from psycopg2 import connect

def apply_k_anonymity(data, k=5):
    # Example logic for anonymization
    print("Applied k-anonymity")

def log_data_access(data_name):
    conn = connect(
        host="localhost",
        port=5432,
        user="admin",
        password="password",
        dbname="hamf_db"
    )
    cur = conn.cursor()
    cur.execute("UPDATE data_inventory SET last_accessed = NOW() WHERE data_name = %s", (data_name,))
    conn.commit()
    conn.close()
