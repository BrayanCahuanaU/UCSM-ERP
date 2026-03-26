<template>
  <div>
    <!-- Barra azul -->
    <div style="width:100%; background:#010B6F; color:white; padding:12px 20px; display:flex;
                justify-content:space-between; align-items:center; box-sizing:border-box;">
      <!-- Texto izquierda -->
      <div style="font-weight:bold; font-size:18px; line-height:1;">
         ERP <span style="color:yellow; font-style:italic;">Universitario</span>
      </div>
      <!-- HOME derecha -->
      <div @click="irHome" style="cursor:pointer; font-size:22px; line-height:1; display:flex;
                                  align-items:center; justify-content:center; padding:4px 8px;">
        🏠
      </div>
    </div>
    <!-- Barra gris - Título y usuario -->
    <div style="width:100%; background:#E5E5E5; padding:10px 20px; display:flex; justify-content:space-between;
                align-items:center; box-sizing:border-box;">
      <!-- Izquierda -->
      <div style="font-weight:bold;">
        {{pcTitulo}}
      </div>
      <!-- Derecha -->
      <div style="font-weight:bold;">
        {{pcNombre}}
      </div>
    </div>
    <!-- Barra de menú - Navegación -->
    <div style="width:100%; background:#F5F5F5; padding:8px 20px; display:flex; gap:15px;
                align-items:center; box-sizing:border-box; border-bottom:1px solid #ddd;">
      <button 
        @click="irA('/dhb1140')" 
        :style="{ 
          backgroundColor: esActivo('/dhb1140') ? '#010B6F' : '#E5E5E5',
          color: esActivo('/dhb1140') ? 'white' : 'black'
        }"
        style="padding:8px 16px; border:none; cursor:pointer; border-radius:4px; font-weight:500; transition:all 0.3s;">
        📋 Equipos
      </button>
      <button 
        @click="irA('/tes1100')" 
        :style="{ 
          backgroundColor: esActivo('/tes1100') ? '#010B6F' : '#E5E5E5',
          color: esActivo('/tes1100') ? 'white' : 'black'
        }"
        style="padding:8px 16px; border:none; cursor:pointer; border-radius:4px; font-weight:500; transition:all 0.3s;">
        📝 Tesis (BDT)
      </button>
      <button 
        @click="irA('/tes1110')" 
        :style="{ 
          backgroundColor: esActivo('/tes1110') ? '#010B6F' : '#E5E5E5',
          color: esActivo('/tes1110') ? 'white' : 'black'
        }"
        style="padding:8px 16px; border:none; cursor:pointer; border-radius:4px; font-weight:500; transition:all 0.3s;">
        ✏️ Revisar (PDT)
      </button>
      <button 
        @click="irA('/tes1120')" 
        :style="{ 
          backgroundColor: esActivo('/tes1120') ? '#010B6F' : '#E5E5E5',
          color: esActivo('/tes1120') ? 'white' : 'black'
        }"
        style="padding:8px 16px; border:none; cursor:pointer; border-radius:4px; font-weight:500; transition:all 0.3s;">
        👨‍🏫 Asesor
      </button>
      <div style="flex:1;"></div>
      <button 
        @click="irLogout" 
        style="padding:8px 16px; border:none; cursor:pointer; border-radius:4px; font-weight:500; 
               background:#d32f2f; color:white; transition:all 0.3s; hover:background:#b71c1c;">
        🚪 Salir
      </button>
    </div>
  </div>
</template>

<script setup>
   import {useRouter, useRoute} from 'vue-router'
   import {ref, onMounted} from 'vue'

   defineProps({
      pcTitulo: {type: String, required: true}
   })

   const router = useRouter()
   const route = useRoute()
   const pcNombre = ref('')

   onMounted(() => {
      let lcNombre = sessionStorage.getItem('GCNOMBRE')
      if (lcNombre) {
         pcNombre.value = lcNombre;
      }
   })

   function irHome() {
      router.push('/');
   }

   function irA(lcPath) {
      router.push(lcPath);
   }

   function irLogout() {
      sessionStorage.clear();
      router.push('/login');
   }

   function esActivo(lcPath) {
      return route.path === lcPath;
   }
</script>
