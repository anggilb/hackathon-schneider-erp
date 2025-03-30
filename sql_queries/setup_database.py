import sqlite3

DB_FILE = "sql_queries/erp.db"


# Execute SQL file
def setup_database(file):
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()

    with open(file, "r") as f:
        sql_script = f.read()

    cur.executescript(sql_script)  # Executes the SQL file
    conn.commit()
    cur.close()
    conn.close()
    print("Database setup completed.")


if __name__ == "__main__":
    file = "sql_queries/setup.sql"
    setup_database(file)
