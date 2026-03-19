<template>
  <button
    @click="$emit('click')"
    :style="buttonStyle"
    @mousedown="presionado = true"
    @mouseup="presionado = false"
    @mouseleave="presionado = false"
  >
    {{ texto }}
  </button>
</template>

<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  texto: {
    type: String,
    default: 'BOTÓN'
  },
  color: {
    type: String,
    default: 'azul' // azul por defecto
  }
})

const presionado = ref(false)

// 🎨 Configuración de colores
const colores = {
  azul: {
    gradiente: 'linear-gradient(to bottom, #0215a8, #010B6F)',
    sombra: '#000a4d'
  },
  rojo: {
    gradiente: 'linear-gradient(to bottom, #d90429, #9d0208)',
    sombra: '#6a040f'
  }
}

const buttonStyle = computed(() => {
  const config = colores[props.color] || colores.azul

  return {
    width: '100%',
    padding: '10px',
    background: config.gradiente,
    color: 'white',
    border: 'none',
    borderRadius: '6px',
    fontWeight: 'bold',
    cursor: 'pointer',
    transition: 'all 0.15s ease',
    transform: presionado.value ? 'translateY(4px)' : 'translateY(0px)',
    boxShadow: presionado.value
      ? `0 2px 0 ${config.sombra}`
      : `0 6px 0 ${config.sombra}, 0 8px 15px rgba(0,0,0,0.3)`
  }
})
</script>
