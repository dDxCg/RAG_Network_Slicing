import sqlite3

conn = sqlite3.connect("kb_log.db")
cursor = conn.cursor()

# CREATE TABLE
cursor.execute("""
CREATE TABLE IF NOT EXISTS exp (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    embb REAL,
    urllc REAL,
    mmtc REAL,
    walk REAL,
    vehicle REAL,
    stationary REAL,
    ue_arrival REAL,
    analyze TEXT,
    action TEXT,
    reward REAL
)
""")
conn.commit()

# IMPORT:
import json
with open("sample_kb.jsonl", "r") as f:
    for line in f:
        obj = json.loads(line)

        numeric = json.loads(obj["numeric_data"])

        cursor.execute("""
        INSERT INTO exp
        (embb, urllc, mmtc, walk, vehicle, stationary, ue_arrival, analyze, action, reward)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            numeric[0],
            numeric[1],
            numeric[2],
            numeric[3],
            numeric[4],
            numeric[5],
            numeric[6],
            json.dumps(obj["analyze"]),
            obj["action"],  
            obj["reward"]
        ))
conn.commit()

# SELECT
# cursor.execute("SELECT * FROM experiences LIMIT 5")
# rows = cursor.fetchall()
# for row in rows:
#     print(row)

# DELETE
# cursor.execute("DELETE FROM experiences")
# cursor.execute("DELETE FROM sqlite_sequence WHERE name='experiments'")

conn.commit()
conn.close()