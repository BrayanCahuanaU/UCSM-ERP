# Backend ERP - Estructura Consolidada

## 📋 Descripción General

Backend FastAPI para sistema de gestión de tesis y equipos de laboratorio. Proporciona endpoints para:
- Autenticación de usuarios
- Gestión de equipos de laboratorio
- Ciclo completo de tesis: BDT → PDT → Asesor

---

## 📁 Estructura de Archivos Activos

```
BackendERP/
├── main.py              # API principal (FastAPI)
├── CSql.py              # Conexión PostgreSQL
├── CTesis.py            # Lógica de tesis (consolidado)
├── CBase.py             # Utilidades base (funciones de fecha, bitácora)
├── API_REFERENCE.md     # Referencia completa de endpoints
├── CONSOLIDACION.md     # Detalles de cambios realizados
└── venv/                # Virtual environment
```

### Archivos Deprecados (referencia histórica)
```
├── _DEPRECATED_1.py         # Métodos antiguos → consolidados en CTesis.py
├── _DEPRECATED_main1.py     # API antigua → consolidada en main.py
└── _DEPRECATED_p99.py       # Script de prueba histórico
```

---

## 🚀 Inicio Rápido

### 1. Activar Virtual Environment
```bash
cd /home/cawibycat/UCSM/Practicas/BackendERP
source venv/bin/activate
```

### 2. Iniciar Servidor
```bash
uvicorn main:app --reload --port 8000
```

Debería ver:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete
```

### 3. Probar Endpoint (en otra terminal)
```bash
curl -X POST http://localhost:8000 \
  -H "Content-Type: application/json" \
  -d '{"ID":"TES1101","CUNIACA":"0049"}'
```

---

## 📚 Archivos Principales

### **main.py** - API FastAPI
- Entrada principal de la aplicación
- Define todos los endpoints POST
- Enruta solicitudes a CTesis o CSql según tipo de operación

**Endpoints principales:**
- `LOG0001` → Login
- `DHB0016` → Lista equipos
- `DHB0017` → Detalle equipo
- `TES11xx` → Líneas de investigación
- `TES1010x` → BDT (Init, Buscar, Grabar)
- `TES1020x` → PDT (Init, Cargar, Grabar dictaminadores)
- `TES1030x` → Revisión PDT (Observar, Aprobar)
- `TES1040x` → Asesor BDT (Init, Buscar, Grabar)

### **CTesis.py** - Lógica de Negocio
Clase `CTesis()` con métodos organizados en grupos:

**Validación de Parámetros:**
- `mxValParamCodigoUsuario()` - Valida formato usuario
- `mxValParamDNI()` - Valida formato DNI
- `mxValParamCodigoEstudiante()` - Valida formato código
- `mxValParamUnidadAcademica()` - Valida unidad académica
- `mxValParamIdTesis()` - Valida ID de tesis

**Tesis - Borrador (BDT):**
- `omInitTesis()` - Inicializa form
- `omBuscarEgresadoTesis()` - Busca estudiante
- `omGrabarPlanTesis()` - Graba BDT

**Tesis - Plan (PDT):**
- `omInitAsignarDictaminadoresPDT()` - Init asignación
- `omCargarDictaminadoresPDT()` - Carga disponibles
- `omGrabarDictaminadoresPDT()` - Asigna 2 dictaminadores

**Tesis - Revisión:**
- `omObservarPDT()` - Agrega observaciones
- `omAprobarPDT()` - Aprueba (requiere 2 aprobaciones)

**Tesis - Asesor:**
- `omInitAsignarAsesorBDT()` - Init asignación asesor
- `omBuscarDocente()` - Busca docentes
- `omGrabarAsesorBDT()` - Asigna asesor

### **CSql.py** - Conexión Base de Datos
Clase `CSql()` que maneja conexión PostgreSQL:
- `omConnect()` - Conecta a DBERP
- `omExecRS()` - Ejecuta SELECT y retorna cursor
- `fetch()` - Obtiene siguiente fila
- `omExec()` - Ejecuta INSERT/UPDATE
- `omCommit()` - Confirma transacción
- `omDisconnect()` - Cierra conexión

**Configuración:**
```python
lcConnect = "host=localhost dbname=DBERP port=5432 user=postgres password=root"
```

### **CBase.py** - Utilidades
- `CDate` - Clase con funciones de fecha
- `fxCorrelativo()` - Genera códigos 0001→0002→...→9999→A000
- `fxBitacora()` - Maneja auditoría JSON
- Funciones auxiliares de hora y día

---

## 🔄 Flujo de Datos - Ejemplo: Registrar Tesis

### 1. Frontend envía: TES1010i
```json
{"ID":"TES1010i","CCODEST":"003WOQ"}
```

### 2. main.py recibe y delega
```python
elif body["ID"] == "TES1010i":
    lo = CTesis()
    lo.paData = body
    llOk = lo.omInitTesis()
```

### 3. CTesis.omInitTesis() ejecuta
```python
llOk = self.mxValParamCodigoEstudiante()  # Valida
llOk = self.loSql.omConnect()             # Conecta BD
llOk = self.mxInitTesis()                 # Ejecuta queries
llOk = self.mxCargarLineas()              # Carga líneas
self.loSql.omDisconnect()                 # Desconecta
```

### 4. CTesis.mxInitTesis() ejecuta SELECT
```sql
SELECT A.cUniAca, B.cNomUni, A.dEgreso FROM A01MEST A 
INNER JOIN A01MUAC B ON B.cUniAca = A.cUniAca
WHERE A.cCodEst = '003WOQ'
```

### 5. CSql.omExecRS() retorna cursor
```python
lcCursor = self.h.cursor()
lcCursor.execute(lcSql)
return lcCursor
```

### 6. CTesis.mxCargarLineas() itera resultados
```python
laTmp = self.loSql.fetch(RS)
while laTmp != None:
    laDatos.append({'CLINEA': laTmp[0], ...})
    laTmp = self.loSql.fetch(RS)
```

### 7. main.py retorna respuesta
```json
{
  "CUNIACA":"0049",
  "CNOMUNI":"INGENIERÍA INFORMÁTICA",
  "DATOS":[...]
}
```

---

## 🐛 Troubleshooting

### "ERROR AL CONECTAR CON LA BASE DE DATOS"
**Causa:** PostgreSQL no disponible o credenciales incorrectas

**Solución:**
```bash
# Verificar PostgreSQL está activo
sudo systemctl status postgresql

# Probar conexión directa
psql "host=localhost port=5432 dbname=DBERP user=postgres password=root"

# Si DB no existe, crear
sudo -u postgres createdb DBERP
```

### "ModuleNotFoundError: No module named 'fastapi'"
**Causa:** Virtual environment no activado

**Solución:**
```bash
source venv/bin/activate
pip install fastapi uvicorn psycopg2-binary
```

### Cambios no reflejados
**Causa:** Servidor no en modo reload

**Solución:**
```bash
# Reiniciar con --reload
uvicorn main:app --reload --port 8000
```

---

## 📊 Base de Datos - Tablas Clave

| Tabla | Descripción |
|-------|-------------|
| S01MUSU | Usuarios |
| S01MPER | Personas (DNI, nombre, contraseña) |
| A01MEST | Estudiantes (código, DNI, unidad académica) |
| A01MUAC | Unidades Académicas |
| A02MLIN | Líneas de Investigación |
| A03MTES | Planes de Tesis (ID, estado, bitácora) |
| A03DEST | Egresados en Tesis (relación tesis-estudiante) |
| A03DDOC | Dictaminadores/Asesores de Tesis |

---

## 🔍 Testing

### Usando p99.py (referencias)
```bash
python _DEPRECATED_p99.py
```

### Usando curl
```bash
# Test TES1101
curl -X POST http://localhost:8000 \
  -H "Content-Type: application/json" \
  -d '{"ID":"TES1101","CUNIACA":"0049"}'
```

### Usando Postman
1. Crear solicitud POST a `http://localhost:8000`
2. Body → raw → JSON
3. Pegarel JSON del endpoint

---

## 📝 Logs

Los logs aparecen en la consola donde corre uvicorn:
```
INFO:     127.0.0.1:12345 - "POST / HTTP/1.1" 200
```

Para más detalle, ver print() en main.py:
```python
print(laData)  # Entrada
return lo.paData  # Salida
```

---

## 🔐 Seguridad (⚠️ TODO)

**Advertencia:** El código actual es vulnerable a:
- SQL Injection (usar parámetros preparados)
- Acceso sin autenticación real
- Contraseñas en claro

**Mejoras necesarias:**
```python
# ❌ Actual (vulnerable)
lcSql = f"WHERE cCodUsu = '{lcCodigoUsu}'"

# ✅ Mejorado (seguro)
lcCursor.execute("WHERE cCodUsu = %s", (lcCodigoUsu,))
```

---

## 📞 Soporte

Para más información ver:
- `API_REFERENCE.md` - Especificación de endpoints
- `CONSOLIDACION.md` - Detalles de cambios
- `CTesis.py` - Documentación en comentarios

