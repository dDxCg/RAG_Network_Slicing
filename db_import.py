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
    content TEXT
)
""")
conn.commit()

# IMPORT:
import json
with open("sample_kb.jsonl", "r") as f:
    for line in f:
        obj = json.loads(line)

        numeric = json.loads(obj["numeric_data"])
        content = f"<ENV>{obj['slice']}. {obj['ue_pattern']}. {obj['ue_arrival']}\n<THINK>{obj['analyze']}\n<ACTION>{obj['action']}\n<REWARD>{obj['reward']}"
        cursor.execute("""
        INSERT INTO exp
        (embb, urllc, mmtc, walk, vehicle, stationary, ue_arrival, content)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            numeric[0],
            numeric[1],
            numeric[2],
            numeric[3],
            numeric[4],
            numeric[5],
            numeric[6],
            content
        ))
conn.commit()
conn.close()