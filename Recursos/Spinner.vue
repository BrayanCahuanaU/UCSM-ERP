<template>
  <div class="spinner"></div>
</template>

<script setup>
// No necesita lógica por ahora
</script>

<style scoped>
.spinner {
  display: inline-block;
  width: 16px;
  height: 16px;
  border: 3px solid #ccc;
  border-top: 3px solid #010B6F;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
</style>
