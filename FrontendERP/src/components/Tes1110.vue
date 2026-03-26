<template>
   <div>
      <LayoutBar pcTitulo="REGISTRO DEL PLAN DE TESIS"/>
      <div style="padding:20px; width:100%; box-sizing:border-box;">
         <div style="width:55%; margin:0 auto;">

            <!-- Datos del estudiante -->
            <div style="margin-bottom:16px; padding:10px; background:#f9f9f9; border:1px solid #ddd; border-radius:4px;">
               <label style="font-weight:bold;">ESTUDIANTE:</label>
               <span style="margin-left:10px;">{{ pcNroDni }} – {{ pcCodest }} – {{ pcNombre }}</span>
            </div>

            <!-- Línea -->
            <div style="margin-bottom:16px;">
               <label style="font-weight:bold; display:block; margin-bottom:6px;">LÍNEA:</label>
               <div v-if="plLoading" style="text-align:center; padding:10px;">
                  <Spinner/>
               </div>
               <select v-else v-model="pcLinea" style="width:100%; padding:8px; font-size:14px; border:1px solid #ccc; border-radius:4px;">
                  <option disabled value="">-- Seleccione una línea --</option>
                  <option v-for="(laItem, index) in paLineas" :key="index" :value="laItem.CLINEA">
                     {{ laItem.CLINEA }} – {{ laItem.CDESCRI }}
                  </option>
               </select>
            </div>

            <!-- Título -->
            <div style="margin-bottom:24px;">
               <label style="font-weight:bold; display:block; margin-bottom:6px;">TÍTULO:</label>
               <textarea
                  v-model="pcTitulo"
                  rows="5"
                  maxlength="500"
                  placeholder="Ingrese el título del plan de tesis..."
                  style="width:100%; padding:8px; font-size:14px; border:1px solid #ccc; border-radius:4px; resize:vertical; box-sizing:border-box;"
               ></textarea>
               <div style="text-align:right; font-size:12px; color:#999;">{{ pcTitulo.length }}/500</div>
            </div>

            <!-- Botones -->
            <div style="display:flex; justify-content:flex-end; gap:10px;">
               <Boton3D color="rojo"  texto="VOLVER" style="width:120px;" @click="f_Volver"/>
               <Boton3D color="verde" texto="GRABAR" style="width:120px;" @click="f_Grabar"/>
            </div>

         </div>
      </div>
   </div>
</template>

<script setup>
   import LayoutBar from '@/components/LayoutBar.vue'
   import Boton3D   from '@/components/Boton3D.vue'
   import Spinner   from '@/components/Spinner.vue'
   import { ref, onMounted } from 'vue'
   import { useRouter } from 'vue-router'

   const poRouter  = useRouter()
   const plLoading = ref(false)

   // Datos del estudiante
   const pcNroDni  = ref('')
   const pcNombre  = ref('')
   const pcCodest  = ref('')
   const pcUniAca  = ref('')

   // Formulario
   const paLineas  = ref([])
   const pcLinea   = ref('')
   const pcTitulo  = ref('')

   onMounted(() => {
      f_Init()
   })

   function f_Init() {
      // Leer datos de sesión
      const lcUsuario   = sessionStorage.getItem('USUARIO')
      const lcSeleccion = sessionStorage.getItem('TES_SELECCION')

      if (!lcUsuario || !lcSeleccion) {
         alert('SESIÓN NO INICIADA')
         poRouter.push('/')
         return
      }

      const loUsuario   = JSON.parse(lcUsuario)
      const loSeleccion = JSON.parse(lcSeleccion)

      pcNroDni.value = loUsuario.CNRODNI   || ''
      pcNombre.value = loUsuario.CNOMBRE   || ''
      pcCodest.value = loSeleccion.CCODEST || ''
      pcUniAca.value = loSeleccion.CUNIACA || ''

      f_CargarLineas()
   }

   async function f_CargarLineas() {
      try {
         plLoading.value = true
         const loRpta = await fetch('http://localhost:8000', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ ID: 'TES1101', CUNIACA: pcUniAca.value })
         })
         if (!loRpta.ok) throw new Error('Error en el servidor')
         const laData = await loRpta.json()
         if (laData.ERROR) {
            alert(laData.ERROR)
            return
         }
         paLineas.value = laData
      } catch (e) {
         console.error(e)
         alert('ERROR AL CARGAR LÍNEAS')
      } finally {
         plLoading.value = false
      }
   }

   async function f_Grabar() {
      if (!pcLinea.value) {
         alert('DEBE SELECCIONAR UNA LÍNEA')
         return
      }
      if (!pcTitulo.value.trim()) {
         alert('DEBE INGRESAR EL TÍTULO')
         return
      }

      try {
         plLoading.value = true
         const loRpta = await fetch('http://localhost:8000', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
               ID:      'TES1102',
               CNRODNI: pcNroDni.value,
               CCODEST: pcCodest.value,
               CUNIACA: pcUniAca.value,
               CLINEA:  pcLinea.value,
               CTITULO: pcTitulo.value.trim()
            })
         })
         if (!loRpta.ok) throw new Error('Error en el servidor')
         const laData = await loRpta.json()
         if (laData.ERROR) {
            alert(laData.ERROR)
            return
         }
         alert('PLAN DE TESIS REGISTRADO CORRECTAMENTE')
         poRouter.push({ name: 'Tes1100' })
      } catch (e) {
         console.error(e)
         alert('ERROR AL GRABAR')
      } finally {
         plLoading.value = false
      }
   }

   function f_Volver() {
      poRouter.push({ name: 'Tes1100' })
   }
</script>
