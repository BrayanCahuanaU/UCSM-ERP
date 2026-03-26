import requests, json
# InitTesis
#laData = {'ID': 'TES1010i', 'CCODEST': '003WOQ'}
#loRpta = requests.post('http://localhost:8000', json=laData)
# BuscarEgresado
#laData = {'ID': 'TES1010b', 'CNRODNI': '73343342', 'CUNIACA': '0049'}
#loRpta = requests.post('http://localhost:8000', json=laData)
# Grabar PDT
laData = {'ID': 'TES1010g', 'CLINEA': '0002', 'CUNIACA': '0049', 'MTITULO': 'TÍTULO DE LA TESIS SIEMPRE DEBE ESTAR EN MAYÚSCULAS',
          'ACODEST': ['003WEP', '003WOQ']}
loRpta = requests.post('http://localhost:8000', json=laData)
#
laData = json.loads(loRpta.text)
print(laData)


#curl -X POST http://localhost:3000/suma -H "Content-Type: application/json" -d '{"ID": "ID", "cusucod": "1221", "a": 7, "b": 4}'
