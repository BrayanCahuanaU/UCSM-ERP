<template>
   <div style="min-height:100vh; background:#f0f0f0; display:flex; flex-direction:column; align-items:center; justify-content:center;">

      <!-- Card -->
      <div style="background:white; border-radius:10px; box-shadow:0 8px 24px rgba(0,0,0,0.15); width:100%; max-width:380px; overflow:hidden;">

         <!-- Header azul -->
         <div style="background:#010B6F; padding:28px 32px; text-align:center;">
            <div style="font-size:22px; font-weight:bold; color:white; letter-spacing:1px;">
               ERP <span style="color:yellow; font-style:italic;">Universitario</span>
            </div>
            <div style="color:#aab4ff; font-size:13px; margin-top:6px;">Ingrese sus credenciales</div>
         </div>

         <!-- Formulario -->
         <div style="padding:32px;">

            <!-- Usuario -->
            <div style="margin-bottom:18px;">
               <label style="display:block; font-weight:bold; font-size:13px; margin-bottom:6px; color:#333;">USUARIO</label>
               <input
                  v-model="pcUsuario"
                  type="text"
                  placeholder="Ingrese su usuario"
                  maxlength="20"
                  @keyup.enter="f_Login"
                  style="width:100%; padding:10px 12px; font-size:14px; border:1px solid #ccc; border-radius:6px; box-sizing:border-box; outline:none;"
                  @focus="e => e.target.style.borderColor='#010B6F'"
                  @blur="e => e.target.style.borderColor='#ccc'"
               />
            </div>

            <!-- Contraseña -->
            <div style="margin-bottom:28px;">
               <label style="display:block; font-weight:bold; font-size:13px; margin-bottom:6px; color:#333;">CONTRASEÑA</label>
               <input
                  v-model="pcClave"
                  type="password"
                  placeholder="Ingrese su contraseña"
                  maxlength="30"
                  @keyup.enter="f_Login"
                  style="width:100%; padding:10px 12px; font-size:14px; border:1px solid #ccc; border-radius:6px; box-sizing:border-box; outline:none;"
                  @focus="e => e.target.style.borderColor='#010B6F'"
                  @blur="e => e.target.style.borderColor='#ccc'"
               />
            </div>

            <!-- Error -->
            <div v-if="pcError" style="background:#fff0f0; border:1px solid #ffcccc; border-radius:6px; padding:10px 14px; margin-bottom:18px; font-size:13px; color:#c0392b;">
               {{ pcError }}
            </div>

            <!-- Botón -->
            <div v-if="plLoading" style="text-align:center; padding:10px;">
               <Spinner/>
            </div>
            <Boton3D v-else texto="INGRESAR" color="azul" @click="f_Login"/>
         </div>

      </div>

      <div style="margin-top:16px; font-size:12px; color:#999;">Sistema ERP — UCSM</div>
   </div>
</template>

<script setup>
   import Boton3D from '@/components/Boton3D.vue'
   import Spinner from '@/components/Spinner.vue'
   import { ref } from 'vue'
   import { useRouter } from 'vue-router'

   const poRouter  = useRouter()
   const pcUsuario = ref('')
   const pcClave   = ref('')
   const pcError   = ref('')
   const plLoading = ref(false)

   async function f_Login() {
      pcError.value = ''

      if (!pcUsuario.value.trim()) {
         pcError.value = 'DEBE INGRESAR EL USUARIO'
         return
      }
      if (!pcClave.value.trim()) {
         pcError.value = 'DEBE INGRESAR LA CONTRASEÑA'
         return
      }

      try {
         plLoading.value = true
         const loRpta = await fetch('http://localhost:8000', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
               ID:      'LOG0001',
               CUSUARIO: pcUsuario.value.trim(),
               CCLAVE:   pcClave.value.trim()
            })
         })

         if (!loRpta.ok) throw new Error('Error en el servidor')

         const laData = await loRpta.json()

         if (laData.ERROR) {
            pcError.value = laData.ERROR
            return
         }

         // Guardar sesión
         sessionStorage.setItem('GCNOMBRE', laData.CNOMBRE)
         sessionStorage.setItem('USUARIO', JSON.stringify({
            CNRODNI: laData.CNRODNI,
            CNOMBRE: laData.CNOMBRE,
            DATOS:   laData.DATOS
         }))

         poRouter.push('/')

      } catch (e) {
         console.error(e)
         pcError.value = 'ERROR AL CONECTAR CON EL SERVIDOR'
      } finally {
         plLoading.value = false
      }
   }
</script>
