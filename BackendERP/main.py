from fastapi import FastAPI
from db import get_connection
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # en producción restringir
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("SELECT COUNT(*) FROM a01mest;")
        result = cur.fetchone()

        cur.close()
        conn.close()

        return {"registros": result[0]}

    except Exception as e:
        return {"error": str(e)}
    
@app.get("/clientes")
def get_clientes():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM a01mest LIMIT 10;")
    rows = cur.fetchall()

    cur.close()
    conn.close()

    return {"data": rows}