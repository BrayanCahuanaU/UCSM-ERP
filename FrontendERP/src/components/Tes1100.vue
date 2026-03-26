<template>
   <div>
      <LayoutBar pcTitulo="REGISTRO DEL PLAN DE TESIS"/>
      <div style="padding:20px; width:100%; box-sizing:border-box;">
         <div style="width:50%; margin:0 auto;">

            <!-- Nombre del estudiante -->
            <div style="margin-bottom:20px; padding:10px; background:#f9f9f9; border:1px solid #ddd; border-radius:4px;">
               <label style="font-weight:bold;">ESTUDIANTE:</label>
               <span style="margin-left:10px;">{{ pcNroDni }} – {{ pcNombre }}</span>
            </div>

            <!-- Select de carreras -->
            <div style="margin-bottom:20px;">
               <label style="font-weight:bold; display:block; margin-bottom:6px;">CARRERA:</label>
               <select v-model="poSeleccion" style="width:100%; padding:8px; font-size:14px; border:1px solid #ccc; border-radius:4px;">
                  <option disabled value="">-- Seleccione una carrera --</option>
                  <option v-for="(laItem, index) in paDatos" :key="index" :value="laItem">
                     {{ laItem.CNOMUNI }}
                  </option>
               </select>
            </div>

            <!-- Botones -->
            <div style="margin-top:25px; display:flex; justify-content:flex-end; gap:10px;">
               <Boton3D color="rojo"  texto="SALIR"   style="width:120px;" @click="f_Salir"/>
               <Boton3D color="verde" texto="APLICAR" style="width:120px;" @click="f_Aplicar"/>
            </div>

         </div>
      </div>
   </div>
</template>

<script setup>
   import LayoutBar from '@/components/LayoutBar.vue'
   import Boton3D   from '@/components/Boton3D.vue'
   import { ref, onMounted } from 'vue'
   import { useRouter } from 'vue-router'

   const poRouter    = useRouter()
   const pcNroDni    = ref('')
   const pcNombre    = ref('')
   const paDatos     = ref([])
   const poSeleccion = ref('')

   onMounted(() => {
      f_Init()
   })

   function f_Init() {
      try {
         const lcData = sessionStorage.getItem('USUARIO')
         if (!lcData) {
            alert('SESIÓN NO INICIADA')
            poRouter.push('/')
            return
         }
         const loData   = JSON.parse(lcData)
         pcNroDni.value = loData.CNRODNI  || ''
         pcNombre.value = loData.CNOMBRE  || ''
         paDatos.value  = loData.DATOS    || []

         if (paDatos.value.length === 0) {
            alert('NO SE ENCONTRARON CARRERAS ASOCIADAS AL ESTUDIANTE')
         }
      } catch (e) {
         console.error('Error leyendo sessionStorage:', e)
         alert('ERROR AL CARGAR DATOS DE SESIÓN')
      }
   }

   function f_Aplicar() {
      if (!poSeleccion.value) {
         alert('DEBE SELECCIONAR UNA CARRERA')
         return
      }
      // Guarda la selección en sessionStorage para la pantalla 1.2
      sessionStorage.setItem('TES_SELECCION', JSON.stringify(poSeleccion.value))
      poRouter.push({ name: 'Tes1110' })
   }

   function f_Salir() {
      poRouter.push('/')
   }
</script>
