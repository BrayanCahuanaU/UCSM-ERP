# Consolidación de Archivos Backend ERP

## Resumen
Se consolidó la lógica distribuida en múltiples archivos en una estructura centralizada para mejorar mantenibilidad y facilitar la ejecución integrada.

---

## Cambios Realizados

### 1. **CTesis.py** (Consolidación)
**Antes:** Contenía solo métodos de tesis básicos (Init, BuscarEgresado, GrabarPlanTesis, Dictaminadores).

**Después:** Se agregaron todos los métodos del archivo `1.py`:
- `omObservarPDT()` / `mxObservarPDT()` - Observaciones en PDT
- `omAprobarPDT()` / `mxAprobarPDT()` - Aprobación de PDT (2 dictaminadores)
- `omInitAsignarAsesorBDT()` / `mxInitAsignarAsesorBDT()` - Init asignación asesor
- `omBuscarDocente()` / `mxBuscarDocente()` - Búsqueda de docentes
- `omGrabarAsesorBDT()` / `mxGrabarAsesorBDT()` - Grabación de asesor

**También:** Se importaron las funciones de utilidad de `CBase.py`:
- `fxCorrelativo()` - Genera códigos correlativos
- `fxBitacora()` - Maneja auditoría

### 2. **main.py** (Consolidación)
**Antes:** Solo endpoints LOG0001, DHB0016, DHB0017, TES1101, TES1102.

**Después:** Se agregaron todos los endpoints de tesis:
- `TES1010i` - Init registro BDT (obtener estudiante + líneas)
- `TES1010b` - Buscar egresado por DNI
- `TES1010g` - Grabar plan de tesis (BDT)
- `TES1020i` - Init asignar dictaminadores PDT
- `TES1020c` - Cargar dictaminadores disponibles
- `TES1020g` - Grabar dictaminadores PDT
- `TES1030o` - Observar PDT (dictaminador comenta)
- `TES1030a` - Aprobar PDT (necesita 2 aprobaciones)
- `TES1040i` - Init asignar asesor BDT
- `TES1040b` - Buscar docente para asesor
- `TES1040g` - Grabar asesor BDT

### 3. **Archivos Deprecados**
Los siguientes archivos quedan como referencia histórica pero no se usan:
- `1.py` → Métodos consolidados en CTesis.py
- `main1.py` → Endpoints consolidados en main.py
- `p99.py` → Script de prueba (referencia)

---

## Flujo Actual de Datos

```
Frontend (Vue.js)
    ↓
main.py (FastAPI)
    ├─ LOG0001 → Login (CSql)
    ├─ DHB0016 → Lista equipos (CSql)
    ├─ DHB0017 → Detalle equipo (CSql)
    ├─ TES11xx → Líneas de investigación (CSql)
    ├─ TES1010i → CTesis.omInitTesis()
    ├─ TES1010b → CTesis.omBuscarEgresadoTesis()
    ├─ TES1010g → CTesis.omGrabarPlanTesis()
    ├─ TES1020i → CTesis.omInitAsignarDictaminadoresPDT()
    ├─ TES1020c → CTesis.omCargarDictaminadoresPDT()
    ├─ TES1020g → CTesis.omGrabarDictaminadoresPDT()
    ├─ TES1030o → CTesis.omObservarPDT()
    ├─ TES1030a → CTesis.omAprobarPDT()
    ├─ TES1040i → CTesis.omInitAsignarAsesorBDT()
    ├─ TES1040b → CTesis.omBuscarDocente()
    └─ TES1040g → CTesis.omGrabarAsesorBDT()
    ↓
CTesis.py (Lógica)
    ↓
CSql.py (Base de datos)
```

---

## Importes Actualizados

**main.py:**
```python
from CTesis import CTesis  # ← Nuevo
```

**CTesis.py:**
```python
from CBase import CDate, fxCorrelativo, fxBitacora  # ← Explícito
```

---

## Próximos Pasos

1. **Frontend (Vue.js):**
   - Completar `Tes1100.vue` (componente de BDT)
   - Completar `Tes1110.vue` (componente de PDT)
   - Conectar con los nuevos endpoints

2. **Backend:**
   - Validación adicional de parámetros si es necesario
   - Manejo de excepciones más robustos
   - Logging mejorado

3. **Testing:**
   - Usar `p99.py` como referencia para pruebas
   - Crear suite de tests unitarios

---

## Estado Actual

✅ Consolidación completada
✅ Endpoints integrados en main.py
✅ Métodos disponibles en CTesis.py
⏳ Componentes Vue pendientes
