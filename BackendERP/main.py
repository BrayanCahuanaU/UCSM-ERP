from fastapi import FastAPI, Request
from db import get_connection
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/")
async def main(request: Request):
    body = await request.json()
    conn = get_connection()
    cur = conn.cursor()

    try:
        if body["ID"] == "DHB0016":
            # LISTA
            cur.execute("""
                SELECT ccodest AS id, cuniaca AS cequipo
                FROM a01mest
                LIMIT 20;
            """)
            rows = cur.fetchall()

            data = []
            for r in rows:
                data.append({
                    "ID": r[0],
                    "CEQUIPO": r[1]
                })

            return data

        elif body["ID"] == "DHB0017":
            # DETALLE
            cur.execute("""
                SELECT 
                    ccodest AS id,
                    cuniaca AS clabora,
                    degreso AS dfecha,
                    cplaest AS ctipmto,
                    cnrodni AS ctecnic,
                    cestado AS cestado
                    FROM a01mest
                LIMIT 10;
            """)
            rows = cur.fetchall()

            return {
                "ID": body["CEQUIPO"],
                "CEQUIPO": body["CEQUIPO"],
                "DATOS": [
                    {
                        "ID": r[0],
                        "CLABORA": r[1],
                        "DFECHA": str(r[2]),
                        "CTIPMTO": r[3],
                        "CTECNIC": r[4],
                        "CESTADO": r[5]
                    } for r in rows
                ]
            }

        else:
            return {"ERROR": "ID no reconocido"}

    except Exception as e:
        return {"ERROR": str(e)}

    finally:
        cur.close()
        conn.close()