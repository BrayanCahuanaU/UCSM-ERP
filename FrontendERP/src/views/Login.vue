<template>
  <div style="display:flex; flex-direction:column; align-items:center; justify-content:center; height:100vh; padding:20px;">
    <div style="max-width:400px; width:100%; border:1px solid #ddd; border-radius:8px; padding:24px; box-shadow:0 2px 10px rgba(0,0,0,0.08);">
      <h1 style="margin:0 0 18px; font-size:24px; text-align:center;">Ingreso</h1>
      <label style="display:block; margin-bottom:10px; font-weight:bold;">Nombre</label>
      <input
        v-model="name"
        type="text"
        placeholder="Ingresa tu nombre"
        style="width:100%; padding:10px; border:1px solid #ccc; border-radius:4px;"
      />
      <button
        @click="onSubmit"
        style="margin-top:16px; width:100%; padding:10px; background:#010B6F; color:#fff; border:none; border-radius:4px; cursor:pointer; font-weight:bold;"
      >
        Ingresar
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const name = ref('')

function onSubmit() {
  if (!name.value.trim()) {
    alert('Por favor ingresa tu nombre')
    return
  }
  sessionStorage.setItem('GCNOMBRE', name.value.trim())
  router.push({ name: 'Mnu1001' })
}
</script>
