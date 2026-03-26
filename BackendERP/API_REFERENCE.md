# API Reference - BackendERP

## Base URL
`http://localhost:8000`

## Autenticación
Todos los endpoints son POST a `/` con JSON body conteniendo `"ID"` que especifica la operación.

---

## Endpoints Disponibles

### 🔐 Autenticación

#### LOG0001: Login
Valida usuario y obtiene datos académicos.

**Request:**
```json
{
  "ID": "LOG0001",
  "CUSUARIO": "codigo_usuario",
  "CCLAVE": "contraseña"
}
```

**Response (éxito):**
```json
{
  "CNRODNI": "73343342",
  "CNOMBRE": "NOMBRE COMPLETO",
  "DATOS": [
    {
      "CCODEST": "003WOQ",
      "CUNIACA": "0049",
      "CNOMUNI": "INGENIERÍA INFORMÁTICA"
    }
  ]
}
```

**Response (error):**
```json
{"ERROR": "USUARIO O CONTRASEÑA INCORRECTOS"}
```

---

### 📚 Equipos Laboratorio (DHB)

#### DHB0016: Listar Equipos
Obtiene lista de equipos de laboratorio.

**Request:**
```json
{
  "ID": "DHB0016",
  "CPERIOD": "2025"
}
```

**Response:**
```json
[
  {"ID": "001", "CEQUIPO": "0049"},
  {"ID": "002", "CEQUIPO": "0050"}
]
```

---

#### DHB0017: Detalle Equipo
Obtiene mantenimientos de un equipo específico.

**Request:**
```json
{
  "ID": "DHB0017",
  "CEQUIPO": "0049",
  "CPERIOD": "2025"
}
```

**Response:**
```json
{
  "ID": "0049",
  "CEQUIPO": "0049",
  "DATOS": [
    {
      "ID": "001",
      "CLABORA": "LAB001",
      "DFECHA": "2025-03-20",
      "CTIPMTO": "MANTENIMIENTO",
      "CTECNIC": "JUAN",
      "CESTADO": "A"
    }
  ]
}
```

---

### 🎓 Tesis - Investigación (TES11xx)

#### TES1101: Cargar Líneas de Investigación
Obtiene líneas de investigación de una unidad académica.

**Request:**
```json
{
  "ID": "TES1101",
  "CUNIACA": "0049"
}
```

**Response:**
```json
[
  {"CLINEA": "0001", "CDESCRI": "SISTEMAS DISTRIBUIDOS"},
  {"CLINEA": "0002", "CDESCRI": "CIBERSEGURIDAD"}
]
```

---

#### TES1102: Grabar Plan de Tesis (antiguo)
*Método antiguo - usar TES1010g en su lugar*

---

### 🎓 Tesis - Borrador (TES1010)

#### TES1010i: Init Registro BDT
Inicializa formulario de registro de Borrador de Tesis obteniendo datos del estudiante y líneas disponibles.

**Request:**
```json
{
  "ID": "TES1010i",
  "CCODEST": "003WOQ"
}
```

**Response:**
```json
{
  "CUNIACA": "0049",
  "CNOMUNI": "INGENIERÍA INFORMÁTICA",
  "DATOS": [
    {"CLINEA": "0001", "CDESCRI": "SISTEMAS DISTRIBUIDOS"},
    {"CLINEA": "0002", "CDESCRI": "CIBERSEGURIDAD"}
  ]
}
```

---

#### TES1010b: Buscar Egresado
Busca estudiante egresado por DNI y unidad académica.

**Request:**
```json
{
  "ID": "TES1010b",
  "CNRODNI": "73343342",
  "CUNIACA": "0049"
}
```

**Response:**
```json
{
  "CNRODNI": "73343342",
  "CCODEST": "003WOQ",
  "CNOMBRE": "JUAN PÉREZ"
}
```

---

#### TES1010g: Grabar Plan de Tesis
Registra el plan de tesis (BDT) con egresados.

**Request:**
```json
{
  "ID": "TES1010g",
  "CLINEA": "0001",
  "CUNIACA": "0049",
  "MTITULO": "DESARROLLO DE PLATAFORMA DE ANÁLISIS DE CIBERSEGURIDAD",
  "ACODEST": ["003WOQ", "003WEP"]
}
```

**Response:**
```json
{"OK": "OK"}
```

---

### 🎓 Tesis - PDT (Plan De Tesis) (TES1020)

#### TES1020i: Init Asignar Dictaminadores
Inicializa lista de tesis aprobadas pendientes de dictaminadores.

**Request:**
```json
{
  "ID": "TES1020i",
  "CCODUSU": "USER"
}
```

**Response:**
```json
{
  "CUNIACA": "0049",
  "CNOMUNI": "INGENIERÍA INFORMÁTICA",
  "DATOS": [
    {
      "CIDTESI": "0001",
      "TPRESEN": "2025-03-20 14:30",
      "MTITULO": "CIBERSEGURIDAD EN APLICACIONES WEB",
      "CLINEA": "0002",
      "CDESLIN": "CIBERSEGURIDAD",
      "CNOMEST": "JUAN PÉREZ",
      "NFLAG": 1
    }
  ]
}
```

---

#### TES1020c: Cargar Dictaminadores
Carga docentes disponibles para asignar como dictaminadores de un plan de tesis.

**Request:**
```json
{
  "ID": "TES1020c",
  "CIDTESI": "0001"
}
```

**Response:**
```json
[
  {"CCODDOC": "DOC1", "CNOMBRE": "DR. PABLO GARCÍA"},
  {"CCODDOC": "DOC2", "CNOMBRE": "ING. CARMEN RODRÍGUEZ"}
]
```

---

#### TES1020g: Grabar Dictaminadores
Asigna los 2 dictaminadores al plan de tesis.

**Request:**
```json
{
  "ID": "TES1020g",
  "CCODUSU": "USER",
  "CIDTESI": "0001",
  "DATOS": [
    {"CCODDOC": "DOC1"},
    {"CCODDOC": "DOC2"}
  ]
}
```

**Response:**
```json
{"OK": "OK"}
```

---

### 🎓 Tesis - Revisión PDT (TES1030)

#### TES1030o: Observar PDT
Dicta minator agrega observaciones al Plan de Tesis.

**Request:**
```json
{
  "ID": "TES1030o",
  "CCODUSU": "DOC1",
  "CIDTESI": "0001",
  "MOBSERV": "El título podría ser más específico. Considere agregar..."
}
```

**Response:**
```json
{"OK": "OK"}
```

---

#### TES1030a: Aprobar PDT
Dictaminador aprueba el Plan de Tesis. Se requiere aprobación de 2 dictaminadores para cambiar estado a 'C'.

**Request:**
```json
{
  "ID": "TES1030a",
  "CCODUSU": "DOC1",
  "CIDTESI": "0001"
}
```

**Response:**
```json
{"OK": "OK"}
```

---

### 🎓 Tesis - Asesor BDT (TES1040)

#### TES1040i: Init Asignar Asesor BDT
Inicializa lista de tesis aprobadas (estado C) pendientes de asesor.

**Request:**
```json
{
  "ID": "TES1040i",
  "CCODUSU": "USER"
}
```

**Response:**
```json
{
  "CUNIACA": "0049",
  "CNOMUNI": "INGENIERÍA INFORMÁTICA",
  "DATOS": [
    {
      "CIDTESI": "0001",
      "TPRESEN": "2025-03-20 14:30",
      "MTITULO": "CIBERSEGURIDAD EN APLICACIONES WEB",
      "CLINEA": "0002",
      "CDESLIN": "CIBERSEGURIDAD",
      "CNOMEST": "JUAN PÉREZ",
      "NFLAG": 1
    }
  ]
}
```

---

#### TES1040b: Buscar Docente
Busca docentes por nombre (búsqueda parcial).

**Request:**
```json
{
  "ID": "TES1040b",
  "CPARAM": "PABLO"
}
```

**Response:**
```json
[
  {"CCODDOC": "DOC1", "CNOMBRE": "DR. PABLO GARCÍA"},
  {"CCODDOC": "DOC5", "CNOMBRE": "LIC. PABLO MARTÍNEZ"}
]
```

---

#### TES1040g: Grabar Asesor BDT
Asigna un asesor al Borrador de Tesis.

**Request:**
```json
{
  "ID": "TES1040g",
  "CCODUSU": "USER",
  "CIDTESI": "0001",
  "CCODDOC": "DOC1"
}
```

**Response:**
```json
{"OK": "OK"}
```

---

## Estados de Tesis

| Estado | Significado | Transición |
|--------|-------------|-----------|
| A | Plan de Tesis Pendiente | Inicial |
| B | Pendiente de Revisión PDT | A → B (asigna dictaminadores) |
| C | PDT Aprobado | B → C (2 dictaminadores aprueban) |
| D | Asesor Asignado | C → D (asigna asesor) |
| E | En Desarrollo | D → E (estudiante avanza) |
| F | Presentado | E → F (sustentación) |
| G | Aprobado | F → G (tribunal aprueba) |
| X | Anulado | Cualquier → X |

---

## Códigos de Error Comunes

```
ERROR AL CONECTAR CON LA BASE DE DATOS
USUARIO O CONTRASEÑA INCORRECTOS
CÓDIGO DE ESTUDIANTE NO EXISTE
ESTUDIANTE TIENE TESIS PENDIENTE
LÍNEA DE INVESTIGACIÓN NO EXISTE
NO HAY DOCENTES QUE CUMPLAN CRITERIO DE BÚSQUEDA
USUARIO NO AUTORIZADO COMO DICTAMINADOR
TESIS NO ESTÁ EN ESTADO APROBADO
ID TESIS NO EXISTE
```

---

## Desarrollo

**Testear endpoints con curl o Postman:**

```bash
curl -X POST http://localhost:8000 \
  -H "Content-Type: application/json" \
  -d '{"ID":"TES1101","CUNIACA":"0049"}'
```

O usar el archivo `_DEPRECATED_p99.py` como referencia de pruebas.

