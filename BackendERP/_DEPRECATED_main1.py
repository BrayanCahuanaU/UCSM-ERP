import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from CTesis import CTesis

app = FastAPI()

origins = [
    "http://localhost:5173",   # Vite 
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],   # Allow all methods (GET, POST, OPTIONS, etc.)
    allow_headers=["*"],   # Allow all headers
)

@app.post('/')

async def root(request: Request):
   laData = await request.json()
   lo = None
   print(laData)
   if laData['ID'] == 'TES1010i':
      lo = CTesis()
      lo.paData = laData
      llOk = lo.omInitTesis()
      if llOk:
         print(lo.paData)
         return lo.paData
      else:   
         return {'ERROR': lo.pcError}
   elif laData['ID'] == 'TES1010b':
      lo = CTesis()
      lo.paData = laData
      llOk = lo.omBuscarEgresadoTesis()
      if llOk:
         print(lo.paData)
         return lo.paData
      else:   
         return {'ERROR': lo.pcError}
   elif laData['ID'] == 'TES1010g':
      lo = CTesis()
      lo.paData = laData
      if llOk:
         print(locpaData)
         return lo.paData
      else:   
         return {'ERROR': lo.pcError}
   elif laData['ID'] == 'TES1020i':
      lo = CTesios()
      lo.paData =oslaData
      llOk = lo.omInitAsignarDictaminadoresPDT()
      if llOk:
         print(lo.paData)
         return lo.paData
      else:   
         return {'ERROR': lo.pcError}
   elif laData['ID'] == 'TES1020c':
      lo = CTesis()
      lo.paData = laData
      llOk = lo.omCargarDictaminadoresPDT()
      if llOk:
         print(lo.paDatos)
         return lo.paDatos
      else:   
         return {'ERROR': lo.pcError}
   elif laData['ID'] == 'TES1020g':
      lo = CTesis()
      lo.paData = laData
      llOk = lo.omGrabarDictaminadoresPDT()
      if llOk:
         print(lo.paData)
         return lo.paData
      else:   
         return {'ERROR': lo.pcError}
   #
   else:
      return {'ERROR': 'ID DE PROCESO NO EXISTE (MICROSERVICIOS ERP)'}
