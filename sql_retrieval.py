import random
import math
def sample_prob(n):
    vals = [random.random() for _ in range(n)]
    s = sum(vals)

    return [v/s for v in vals]

sample_slice_prob = sample_prob(3)
sample_pattern_prob = sample_prob(3)
sample_arrival = random.randrange(-5, 5, 1)
query_numeric = [*sample_slice_prob, *sample_pattern_prob, sample_arrival]

import sqlite3
conn = sqlite3.connect("kb_log.db")
cursor = conn.cursor()

cursor.execute("""
SELECT id, embb, urllc, mmtc, walk, vehicle, stationary, ue_arrival, content,
(embb*? +
 urllc*? +
 mmtc*? +
 walk*? +
 vehicle*? +
 stationary*? +
 ue_arrival*?) AS sim
FROM exp
ORDER BY sim DESC
LIMIT 50
""", query_numeric)

rows = cursor.fetchall()

candidates = []
for row in rows:
    candidates.append({
        "id": row[0],
        "vec": row[1:8],   
        "content": row[8],
        "sim": row[9]      
    })

def mmr(candidates, top_k=5, mmr_lambda=0.7):
    selected = []

    def dot(a,b):
        return sum(x*y for x,y in zip(a,b))
        
    while len(selected) < top_k and candidates:

        best_doc = None
        best_score = -math.inf

        for doc in candidates:
            similarity = doc['sim']
            if not selected:
                diversity = 0
            else:
                diversity = max(dot(doc['vec'], s['vec']) for s in selected)

            mmr_score = mmr_lambda * similarity - (1 - mmr_lambda) * diversity

            if mmr_score > best_score:
                best_score = mmr_score
                best_doc = doc
            
        selected.append(best_doc)
        candidates.remove(best_doc)
    
    return selected


top_k = mmr(candidates)
for doc in top_k:
    print(f"{doc}\n")

