# 📋 Próximos Pasos - Frontend Vue.js

## Estado Actual

✅ **Backend:** Completamente funcional con 15 endpoints activos
⏳ **Frontend:** Componentes parcialmente implementados

---

## Componentes Pendientes

### 1. **Tes1100.vue** - Registro de Borrador de Tesis (BDT)

**Descripción:**
Interfaz para estudiante registrar su plan de tesis (borrador) seleccionando:
- Estudiante/Egresado
- Línea de investigación
- Título de tesis

**Endpoints necesarios:**
```
TES1010i  → Obtener datos iniciales (estudiante + líneas)
TES1010b  → Buscar egresado por DNI
TES1010g  → Grabar plan de tesis
```

**Flujo esperado:**
```
1. Pantalla 1: Ingresar código estudiante
   - Button: [Buscar] → Llama TES1010i
   - Muestra: CUNIACA, CNOMUNI, lista de CLINEA disponibles
   
2. Pantalla 2: Buscar egresado
   - Input: DNI egresado
   - Button: [Buscar] → Llama TES1010b
   - Muestra: CCODEST, CNOMBRE
   
3. Pantalla 3: Ingresar datos tesis
   - Seleccionar CLINEA (dropdown)
   - Input: MTITULO (texto largo)
   - Seleccionar egresados (multi-select)
   - Button: [Grabar] → Llama TES1010g
```

**Estructura Vue recomendada:**
```vue
<template>
  <div>
    <div v-if="pcScreen === '1'"><!-- Init --></div>
    <div v-if="pcScreen === '2'"><!-- Buscar egresado --></div>
    <div v-if="pcScreen === '3'"><!-- Ingresar datos --></div>
  </div>
</template>

<script setup>
const pcScreen = ref('1')
const paData = ref({})
const paDatos = ref([])

async function f_InitTesis() {
  const res = await fetch('http://localhost:8000', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ ID: 'TES1010i', CCODEST: pcCodEst.value })
  })
  const data = await res.json()
  // procesar data
}
</script>
```

---

### 2. **Tes1110.vue** - Revisión de Plan de Tesis (PDT)

**Descripción:**
Interfaz para dictaminadores revisar y aprobar/rechazar el plan de tesis.

**Endpoints necesarios:**
```
TES1020i  → Obtener lista de tesis pendientes (estado A)
TES1020c  → Cargar docentes disponibles para asignar
TES1020g  → Grabar dictaminadores seleccionados
TES1030o  → Agregar observaciones
TES1030a  → Aprobar PDT (cuando está en estado B)
```

**Flujo esperado:**
```
1. Pantalla 1: Lista de tesis pendientes (estado A)
   - Tabla con: CIDTESI, MTITULO, CLINEA, CNOMEST
   - Button por fila: [Asignar Dictaminadores]
   
2. Pantalla 2: Seleccionar 2 dictaminadores
   - Llama TES1020i para cargar lista
   - Para cada fila TES1020c busca docentes disponibles
   - Multi-select: Selecciona exactamente 2
   - Button: [Grabar] → TES1020g
   
3. Pantalla 3: Revisión y aprobación
   - Muestra PDT en estado B
   - TextArea: Observaciones (opcional)
   - Button: [Comentar] → TES1030o
   - Button: [Aprobar] → TES1030a
```

**Estructura Vue recomendada:**
```vue
<template>
  <div>
    <div v-if="pcScreen === '1'"><!-- Lista tesis --></div>
    <div v-if="pcScreen === '2'"><!-- Asignar dictaminadores --></div>
    <div v-if="pcScreen === '3'"><!-- Revisar/Aprobar --></div>
  </div>
</template>

<script setup>
const pcScreen = ref('1')
const paTesis = ref([])
const paDictaminadores = ref([])
const paSeleccionados = ref([])

async function f_CargarTesis() {
  const res = await fetch('http://localhost:8000', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ ID: 'TES1020i', CCODUSU: lcUsuario })
  })
  const data = await res.json()
  paTesis.value = data.DATOS
}
</script>
```

---

### 3. **Componente Asesor BDT** (Nuevo)

**Descripción:**
Interfaz para asignar asesor a tesis aprobadas (estado C).

**Endpoints necesarios:**
```
TES1040i  → Obtener lista de tesis con estado C
TES1040b  → Buscar docentes por nombre
TES1040g  → Grabar asesor
```

**Flujo esperado:**
```
1. Pantalla 1: Lista de tesis aprobadas (estado C)
   - Tabla: CIDTESI, MTITULO, CNOMEST
   - Button: [Asignar Asesor]
   
2. Pantalla 2: Buscar y asignar
   - Input: Nombre docente
   - Button: [Buscar] → TES1040b
   - Tabla: Docentes encontrados
   - Button: [Seleccionar] → TES1040g
```

---

## Orden Recomendado de Implementación

1. **Tes1100.vue** (más simple, inicio del flujo)
   - Tiempo: 2-3 horas
   - Componentes necesarios: Input, Select, Table, Button

2. **Tes1110.vue** (más complejo, múltiples pantallas)
   - Tiempo: 4-5 horas
   - Componentes necesarios: Input, TextArea, MultiSelect, Table

3. **Componente Asesor** (simple, similar a BDT)
   - Tiempo: 2 horas
   - Componentes necesarios: Input, Table, Button

---

## Template de Inicio para Tes1100.vue

```vue
<template>
  <div>
    <LayoutBar pcTitulo="REGISTRO DE BORRADOR DE TESIS"/>
    <div style="padding:20px; width:100%;">
      
      <!-- Pantalla 1: Init -->
      <div v-if="pcScreen === '1'">
        <div style="width:75%; margin:0 auto;">
          <h3>Paso 1: Seleccionar Estudiante</h3>
          <input 
            v-model="pcCodEst" 
            placeholder="Código estudiante"
            @keyup.enter="f_InitTesis"
          />
          <Boton3D color="azul" texto="CONTINUAR" @click="f_InitTesis"/>
        </div>
      </div>

      <!-- Pantalla 2: Buscar egresado -->
      <div v-if="pcScreen === '2'">
        <div style="width:75%; margin:0 auto;">
          <h3>Paso 2: Buscar Egresado</h3>
          <input 
            v-model="pcDNI" 
            placeholder="DNI egresado"
            @keyup.enter="f_BuscarEgresado"
          />
          <Boton3D color="azul" texto="BUSCAR" @click="f_BuscarEgresado"/>
          <div v-if="paEgresado" style="margin-top:20px;">
            <p><strong>Código:</strong> {{paEgresado.CCODEST}}</p>
            <p><strong>Nombre:</strong> {{paEgresado.CNOMBRE}}</p>
          </div>
          <Boton3D color="azul" texto="SIGUIENTE" @click="pcScreen='3'"/>
        </div>
      </div>

      <!-- Pantalla 3: Ingresar datos tesis -->
      <div v-if="pcScreen === '3'">
        <div style="width:75%; margin:0 auto;">
          <h3>Paso 3: Datos de la Tesis</h3>
          <label>Línea de Investigación:</label>
          <select v-model="pcLinea">
            <option v-for="l in paLineas" :key="l.CLINEA" :value="l.CLINEA">
              {{l.CLINEA}} - {{l.CDESCRI}}
            </option>
          </select>
          
          <label>Título de Tesis:</label>
          <textarea v-model="pcTitulo" rows="4"></textarea>
          
          <label>Egresados:</label>
          <div v-for="e in paEgresados" :key="e.CCODEST">
            <input type="checkbox" v-model="paSeleccionados" :value="e.CCODEST"/>
            {{e.CNOMBRE}}
          </div>
          
          <Boton3D color="verde" texto="GRABAR" @click="f_GrabarTesis"/>
        </div>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import LayoutBar from '@/components/LayoutBar.vue'
import Boton3D from '@/components/Boton3D.vue'

const pcScreen = ref('1')
const pcCodEst = ref('')
const pcDNI = ref('')
const pcLinea = ref('')
const pcTitulo = ref('')
const paEgresado = ref(null)
const paLineas = ref([])
const paEgresados = ref([])
const paSeleccionados = ref([])

async function f_InitTesis() {
  const res = await fetch('http://localhost:8000', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ ID: 'TES1010i', CCODEST: pcCodEst.value })
  })
  const data = await res.json()
  if (data.ERROR) {
    alert(data.ERROR)
  } else {
    paLineas.value = data.DATOS
    pcScreen.value = '2'
  }
}

async function f_BuscarEgresado() {
  const res = await fetch('http://localhost:8000', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ 
      ID: 'TES1010b', 
      CNRODNI: pcDNI.value,
      CUNIACA: '0049' // Obtener de login
    })
  })
  const data = await res.json()
  if (data.ERROR) {
    alert(data.ERROR)
  } else {
    paEgresado.value = data
    paEgresados.value = [data] // O cargar lista si hay múltiples
  }
}

async function f_GrabarTesis() {
  const res = await fetch('http://localhost:8000', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ 
      ID: 'TES1010g',
      CLINEA: pcLinea.value,
      CUNIACA: '0049',
      MTITULO: pcTitulo.value,
      ACODEST: paSeleccionados.value
    })
  })
  const data = await res.json()
  if (data.ERROR) {
    alert(data.ERROR)
  } else {
    alert('Tesis grabada exitosamente')
    // Redirigir o resetear
  }
}
</script>
```

---

## Integración con Router

En `router/index.js` ya están definidas las rutas:
```javascript
{path: '/tes1100', name: 'Tes1100', component: Tes1100}
{path: '/tes1110', name: 'Tes1110', component: Tes1110}
```

Navegar desde otros componentes:
```javascript
const router = useRouter()
router.push('/tes1100')  // o
router.push({name: 'Tes1100'})
```

---

## Variables de Contexto Usuario

Desde Login, guardar en localStorage o Pinia:
```javascript
// En Login.vue
const paUsuario = {
  CNRODNI: '73343342',
  CNOMBRE: 'JUAN PÉREZ',
  CCODUSU: 'USER001',
  CUNIACA: '0049'
}
localStorage.setItem('usuario', JSON.stringify(paUsuario))

// En otros componentes
const paUsuario = JSON.parse(localStorage.getItem('usuario'))
const lcCodusu = paUsuario.CCODUSU
```

---

## Testing de Componentes

1. **Iniciar frontend:**
   ```bash
   cd FrontendERP
   npm run dev
   ```

2. **Iniciar backend:**
   ```bash
   cd BackendERP
   source venv/bin/activate
   uvicorn main:app --reload --port 8000
   ```

3. **Abrir en navegador:**
   ```
   http://localhost:5173
   ```

4. **Navegar a nuevos componentes:**
   ```
   http://localhost:5173/tes1100
   http://localhost:5173/tes1110
   ```

---

## Checklist de Implementación

- [ ] **Tes1100.vue**
  - [ ] Pantalla 1: Init estudiante
  - [ ] Pantalla 2: Buscar egresado
  - [ ] Pantalla 3: Ingresar datos
  - [ ] Validación de campos
  - [ ] Manejo de errores
  - [ ] Estilos CSS

- [ ] **Tes1110.vue**
  - [ ] Pantalla 1: Lista tesis (estado A)
  - [ ] Pantalla 2: Asignar dictaminadores
  - [ ] Pantalla 3: Revisar PDT
  - [ ] Observaciones
  - [ ] Aprobación
  - [ ] Estilos CSS

- [ ] **Componente Asesor**
  - [ ] Listar tesis estado C
  - [ ] Buscar docentes
  - [ ] Asignar asesor

---

**Estimado total de desarrollo:** 8-10 horas
