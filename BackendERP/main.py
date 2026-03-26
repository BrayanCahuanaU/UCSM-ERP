from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from CSql import CSql

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

    # ─── LOG0001: Login ───────────────────────────────────────────────────
    if body["ID"] == "LOG0001":
        lcUsuario = body.get("CUSUARIO", "")  # ccodusu de s01musu
        lcClave   = body.get("CCLAVE",   "")  # cclave de s01mper

        loSql = CSql()
        llOk  = loSql.omConnect()
        if not llOk:
            return {"ERROR": loSql.pcError}

        lcSql = f"""
            SELECT U.cnrodni, P.cnombre
            FROM s01musu U
            JOIN s01mper P ON P.cnrodni = U.cnrodni
            WHERE U.ccodusu = '{lcUsuario}'
              AND P.cclave  = '{lcClave}'
              AND U.cestado = 'A'
            LIMIT 1
        """
        RS    = loSql.omExecRS(lcSql)
        laTmp = loSql.fetch(RS)

        if laTmp is None:
            loSql.omDisconnect()
            return {"ERROR": "USUARIO O CONTRASEÑA INCORRECTOS"}

        lcNroDni = laTmp[0].strip()
        lcNombre = laTmp[1].strip()

        lcSql2 = f"""
            SELECT M.ccodest, M.cuniaca, A.cnomuni
            FROM a01mest M
            JOIN a01muac A ON A.cuniaca = M.cuniaca
            WHERE M.cnrodni = '{lcNroDni}'
              AND M.cestado = 'A'
            ORDER BY M.cuniaca
        """
        RS2    = loSql.omExecRS(lcSql2)
        laTmp2 = loSql.fetch(RS2)
        laDatos = []
        while laTmp2 is not None:
            laDatos.append({
                "CCODEST": laTmp2[0].strip() if laTmp2[0] else "",
                "CUNIACA": laTmp2[1].strip() if laTmp2[1] else "",
                "CNOMUNI": laTmp2[2].strip() if laTmp2[2] else ""
            })
            laTmp2 = loSql.fetch(RS2)

        loSql.omDisconnect()
        return {
            "CNRODNI": lcNroDni,
            "CNOMBRE": lcNombre,
            "DATOS":   laDatos
        }

    # ─── DHB0016: Lista equipos ───────────────────────────────────────────
    elif body["ID"] == "DHB0016":
        loSql = CSql()
        llOk  = loSql.omConnect()
        if not llOk:
            return {"ERROR": loSql.pcError}

        lcSql = """
            SELECT ccodest, cuniaca
            FROM a01mest
            LIMIT 20
        """
        RS    = loSql.omExecRS(lcSql)
        laTmp = loSql.fetch(RS)
        laDatos = []
        while laTmp is not None:
            laDatos.append({
                "ID":      laTmp[0],
                "CEQUIPO": laTmp[1]
            })
            laTmp = loSql.fetch(RS)

        loSql.omDisconnect()
        return laDatos

    # ─── DHB0017: Detalle equipo ──────────────────────────────────────────
    elif body["ID"] == "DHB0017":
        lcEquipo = body.get("CEQUIPO", "")

        loSql = CSql()
        llOk  = loSql.omConnect()
        if not llOk:
            return {"ERROR": loSql.pcError}

        lcSql = f"""
            SELECT ccodest, cuniaca, degreso, cplaest, cnrodni, cestado
            FROM a01mest
            WHERE cuniaca = '{lcEquipo}'
            LIMIT 10
        """
        RS    = loSql.omExecRS(lcSql)
        laTmp = loSql.fetch(RS)
        laDatos = []
        while laTmp is not None:
            laDatos.append({
                "ID":      laTmp[0],
                "CLABORA": laTmp[1],
                "DFECHA":  str(laTmp[2]),
                "CTIPMTO": laTmp[3],
                "CTECNIC": laTmp[4],
                "CESTADO": laTmp[5]
            })
            laTmp = loSql.fetch(RS)

        loSql.omDisconnect()
        return {
            "ID":      lcEquipo,
            "CEQUIPO": lcEquipo,
            "DATOS":   laDatos
        }

    # ─── TES1101: Cargar líneas de investigación ──────────────────────────
    elif body["ID"] == "TES1101":
        lcUniAca = body.get("CUNIACA", "0049")

        loSql = CSql()
        llOk  = loSql.omConnect()
        if not llOk:
            return {"ERROR": loSql.pcError}

        lcSql = f"SELECT cLinea, cDescri FROM A02MLIN WHERE cUniAca = '{lcUniAca}' ORDER BY cLinea"
        RS    = loSql.omExecRS(lcSql)
        laTmp = loSql.fetch(RS)
        laDatos = []
        while laTmp is not None:
            laDatos.append({"CLINEA": laTmp[0], "CDESCRI": laTmp[1]})
            laTmp = loSql.fetch(RS)

        loSql.omDisconnect()
        return laDatos

    # ─── TES1102: Grabar plan de tesis ────────────────────────────────────
    elif body["ID"] == "TES1102":
        lcNroDni = body.get("CNRODNI", "")
        lcCodest = body.get("CCODEST", "")
        lcUniAca = body.get("CUNIACA", "")
        lcLinea  = body.get("CLINEA",  "")
        lcTitulo = body.get("CTITULO", "").replace("'", "''")

        loSql = CSql()
        llOk  = loSql.omConnect()
        if not llOk:
            return {"ERROR": loSql.pcError}

        lcSql = f"""
            INSERT INTO A03MTES (cnrodni, ccodest, cuniaca, clinea, ctitulo, cestado, dfechre)
            VALUES ('{lcNroDni}', '{lcCodest}', '{lcUniAca}', '{lcLinea}', '{lcTitulo}', 'S', CURRENT_DATE)
        """
        llOk = loSql.omExec(lcSql)
        if not llOk:
            loSql.omDisconnect()
            return {"ERROR": loSql.pcError}

        loSql.omCommit()
        loSql.omDisconnect()
        return {"OK": True}

    else:
        return {"ERROR": "ID no reconocido"}