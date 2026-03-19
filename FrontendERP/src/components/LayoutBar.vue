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
    <!-- Barra gris CORREGIDA -->
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
  </div>
</template>

<script setup>
   import {useRouter} from 'vue-router'
   import {ref, onMounted} from 'vue'

   defineProps({
      pcTitulo: {type: String, required: true}
   })

   const router = useRouter()
   const pcNombre = ref('')

   onMounted(() => {
      let lcNombre = sessionStorage.getItem('GCNOMBRE')
      if (lcNombre) {
         pcNombre.value = lcNombre;
      }
   })

   function irHome() {
      router.push('/login');
   }
</script>
