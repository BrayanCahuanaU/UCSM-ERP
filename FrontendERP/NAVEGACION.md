# 🧭 Navegación Frontend - Guía de Acceso

## Cambios Realizados

Se agregó un **menú de navegación horizontal** en la barra superior del sistema (LayoutBar.vue) que permite cambiar entre secciones sin problemas.

---

## 📍 Estructura de Navegación

### Ubicación
El menú está debajo del nombre del usuario, en una barra gris clara con botones.

### Secciones Disponibles

```
┌─────────────────────────────────────────────────────────────────────┐
│ ERP Universitario                                              👤    │
├─────────────────────────────────────────────────────────────────────┤
│ TÍTULO DE SECCIÓN                                          Usuario   │
├─────────────────────────────────────────────────────────────────────┤
│ [📋 Equipos]  [📝 Tesis (BDT)]  [✏️ Revisar (PDT)]  [👨‍🏫 Asesor]  [🚪 Salir] │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 🎯 Botones del Menú

| Botón | Ruta | Descripción | Estado |
|-------|------|-------------|--------|
| 📋 **Equipos** | `/dhb1140` | Mantenimiento de equipos de laboratorio | ✅ Completo |
| 📝 **Tesis (BDT)** | `/tes1100` | Registro de Borrador de Tesis | ⏳ Pendiente |
| ✏️ **Revisar (PDT)** | `/tes1110` | Revisión del Plan de Tesis | ⏳ Pendiente |
| 👨‍🏫 **Asesor** | `/tes1120` | Asignación de Asesor | ⏳ Pendiente |
| 🚪 **Salir** | `/login` | Cerrar sesión | ✅ Activo |

---

## 🔄 Flujo de Acceso

### Después de Login

```
1. Usuario entra a /login
   ↓
2. Ingresa credenciales (CUSUARIO + CCLAVE)
   ↓
3. Si es correcto → Redirige a / (que es Dhb1140)
   ↓
4. Ve menú de navegación:
   [📋 Equipos]  [📝 Tesis]  [✏️ Revisar]  [👨‍🏫 Asesor]  [🚪 Salir]
   ↓
5. Puede hacer clic en cualquier botón para navegar
```

---

## 💡 Características del Menú

### Botones Activos
- El botón de la sección actual se destaca en **azul oscuro** con texto **blanco**
- Los botones inactivos tienen fondo **gris claro** y texto **negro**

### Ejemplo
Si estás en "Equipos":
```
[📋 Equipos]  (← AZUL OSCURO, ACTIVO)
[📝 Tesis]     (← Gris claro, inactivo)
[✏️ Revisar]   (← Gris claro, inactivo)
[👨‍🏫 Asesor]    (← Gris claro, inactivo)
```

Si haces clic en "Tesis":
```
[📋 Equipos]   (← Gris claro, inactivo)
[📝 Tesis]     (← AZUL OSCURO, ACTIVO)  ← Cambió
[✏️ Revisar]   (← Gris claro, inactivo)
[👨‍🏫 Asesor]    (← Gris claro, inactivo)
```

---

## 🏠 Botón HOME

En la barra azul superior, a la derecha, hay un botón 🏠 que:
- Te lleva a "/" (Equipos)
- Permite regresar rápidamente a la sección principal

---

## 🚪 Salir

El botón **🚪 Salir** en rojo:
- Limpia la sesión
- Te redirige a `/login`
- Debes volver a ingresar credenciales

---

## 📝 Rutas Disponibles (Implementadas)

```javascript
// router/index.js
/login                → Login.vue        (Autenticación)
/                     → Dhb1140.vue      (Equipos - Home)
/dhb1140             → Dhb1140.vue      (Equipos)
/tes1100             → Tes1100.vue      (BDT - Pendiente)
/tes1110             → Tes1110.vue      (PDT - Pendiente)
/tes1120             → Tes1110.vue      (Asesor - Pendiente, usa PDT temporalmente)
```

---

## 🔄 Cambios Técnicos en LayoutBar.vue

### Antes
```vue
<button @click="irHome()">🏠</button>
<!-- Sin menú de navegación -->
```

### Después
```vue
<button @click="irA('/dhb1140')" :style="{ backgroundColor: esActivo('/dhb1140') ? '#010B6F' : '#E5E5E5' }">
  📋 Equipos
</button>
<!-- ... más botones -->
<button @click="irLogout()">🚪 Salir</button>
```

### Nuevas Funciones
```javascript
function irA(lcPath) {
  router.push(lcPath)  // Navega a ruta
}

function irLogout() {
  sessionStorage.clear()  // Limpia sesión
  router.push('/login')   // Redirige a login
}

function esActivo(lcPath) {
  return route.path === lcPath  // Detecta ruta actual
}
```

---

## 🧪 Cómo Probar

### 1. Iniciar aplicación
```bash
cd /home/cawibycat/UCSM/Practicas/FrontendERP
npm run dev
```

### 2. Abrir en navegador
```
http://localhost:5173
```

### 3. Login
- Usuario: `USER001` (o válido en BD)
- Contraseña: `PASS123`

### 4. Ver menú
Después de autenticarse, verás:
```
[📋 Equipos]  [📝 Tesis]  [✏️ Revisar]  [👨‍🏫 Asesor]  [🚪 Salir]
```

### 5. Hacer clic
- Haz clic en "📝 Tesis" 
  → Navega a `/tes1100` (mostrará página de BDT)
- Haz clic en "✏️ Revisar"
  → Navega a `/tes1110` (mostrará página de PDT)
- Haz clic en "👨‍🏫 Asesor"
  → Navega a `/tes1120` (mostrará página de Asesor)

---

## 📊 Estado de Implementación

| Componente | Navegación | Contenido | Estado |
|------------|-----------|----------|--------|
| Dhb1140 | ✅ Visible | ✅ Completo | **LISTO** |
| Tes1100 | ✅ Visible | ⏳ Parcial | **EN DESARROLLO** |
| Tes1110 | ✅ Visible | ⏳ Parcial | **EN DESARROLLO** |
| Tes1120 | ✅ Visible | ⏳ Temporal | **PENDIENTE** |

---

## 🚀 Próximos Pasos

1. **Completar Tes1100.vue**
   - Implementar flujo de 3 pantallas
   - Conectar con endpoints TES1010x

2. **Completar Tes1110.vue**
   - Implementar flujo de revisión PDT
   - Conectar con endpoints TES1020x, TES1030x

3. **Crear Tes1120.vue**
   - Componente para asignación de asesor
   - Conectar con endpoints TES1040x

---

## 💻 Archivos Modificados

```
FrontendERP/src/
├── components/
│   └── LayoutBar.vue       [MODIFICADO] - Agregó menú de navegación
└── router/
    └── index.js            [MODIFICADO] - Agregó rutas faltantes
```

---

## 📌 Resumen

**Problema:** No había forma de navegar entre secciones después de login.

**Solución:** 
- Agregué menú horizontal en `LayoutBar.vue`
- Agregué rutas faltantes en `router/index.js`
- El menú es dinámico y muestra qué sección estás visitando
- El menú es accesible desde cualquier sección

**Resultado:** Ahora puedes:
- ✅ Navegar libremente entre secciones
- ✅ Ver qué sección estás visitando (botón destacado)
- ✅ Salir de la sesión
- ✅ Volver al home con el botón 🏠

