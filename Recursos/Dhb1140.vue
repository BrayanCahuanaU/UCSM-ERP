<template>
   <div>
      <LayoutBar pcTitulo="MANTENIMIENTO EQUIPOS LABORATORIO"/>
      <div style="padding:20px; width:100%; box-sizing:border-box;">
         <div v-if="pcScreen === '1'">
            <div style="width:75%; margin:0 auto;">
               <div style="padding:0px; margin-top:0px;">
               <div style="margin-bottom:5px;">
                  <label style="font-weight:bold; margin-right:10px;">PERIODO:</label>
                  <input v-model="pcPeriod" maxlength="4" inputmode="numeric" autofocus @input="pcPeriod = pcPeriod.replace(/[^0-9]/g,'')" style="padding:6px; width:100px; font-size:14px;">
               </div>
               </div>
               <div style="margin:0 auto;">
                  <div v-if="plLoading" style="text-align:center; width:100%; margin-top:20px;">
                     <Spinner />
                  </div>
                  <div v-if="!plLoading && paDatos" style="width:100%; max-height:400px; overflow-y:auto; border:1px solid #ccc; margin-top:10px;">
                     <table border="1" style="width:100%; border-collapse:collapse; font-size:14px;">
                        <thead>
                           <tr style="background:#f2f2f2;">
                           <th style="padding:6px; position:sticky; top:0; background:#f2f2f2; text-align:center;">#</th>
                           <th style="padding:6px; position:sticky; top:0; background:#f2f2f2; text-align:center;">ID</th>
                           <th style="padding:6px; position:sticky; top:0; background:#f2f2f2; text-align:left;">LABORATORIO</th>
                           <th style="padding:6px; position:sticky; top:0; background:#f2f2f2; text-align:center;">🔎</th>
                           </tr>
                        </thead>
                        <tbody>
                           <tr v-for="(laItem, index) in paDatos" :key="index">
                              <td style="padding:6px; text-align:center;">{{index + 1}}</td>
                              <td style="padding:6px; text-align:center;">{{laItem.ID}}</td>
                              <td style="padding:6px; text-align:left;">{{laItem.CEQUIPO}}</td>
                              <td style="padding:6px; text-align:center; cursor:pointer;" @click="f_Detalle(laItem.CEQUIPO)" title="Ver detalle">🔎</td>
                           </tr>
                           <tr v-if="!paDatos.length">
                              <td colspan="4" style="padding:10px; text-align:center;">
                                 NO SE ENCONTRARON REGISTROS
                              </td>
                           </tr>
                        </tbody>
                     </table>
                  </div>
                  <!-- Botón Regresar -->
                  <div style="margin-top:15px; text-align:right;">
                     <Boton3D color="rojo" texto="SALIR" style="width:10%;" @click="f_Salir"></Boton3D>
                  </div>
               </div>
            </div>
         </div>
         <div v-if="pcScreen === '2'">
            <div style="margin-bottom:10px; font-weight:bold;">
               EQUIPO: {{pcIdEqui}} - {{pcEquipo}}
            </div>
            <div v-if="plLoading" style="text-align:center; width:100%; margin-top:20px;">
               <Spinner />
            </div>
            <div v-if="!plLoading && paData" style="width:100%; max-height:400px; overflow-y:auto; border:1px solid #ccc;">
               <table border="1" style="width:100%; border-collapse:collapse; font-size:14px;">
                  <thead>
                     <tr style="background:#f2f2f2;">
                     <th style="padding:6px; position:sticky; top:0; background:#f2f2f2; text-align:center;">#</th>
                     <th style="padding:6px; position:sticky; top:0; background:#f2f2f2; text-align:center;">ID</th>
                     <th style="padding:6px; position:sticky; top:0; background:#f2f2f2; text-align:center;">LABORATORIO</th>
                     <th style="padding:6px; position:sticky; top:0; background:#f2f2f2; text-align:center;">FECHA</th>
                     <th style="padding:6px; position:sticky; top:0; background:#f2f2f2; text-align:left;">MANTENIMIENTO</th>
                     <th style="padding:6px; position:sticky; top:0; background:#f2f2f2; text-align:center;">´TÉCNICO</th>
                     <th style="padding:6px; position:sticky; top:0; background:#f2f2f2; text-align:left;">ESTADO</th>
                     </tr>
                  </thead>
                  <tbody>
                     <tr v-for="(laItem, index) in paData.DATOS" :key="index">
                        <td style="padding:6px; text-align:center;">{{index + 1}}</td>
                        <td style="padding:6px; text-align:center;">{{laItem.ID}}</td>
                        <td style="padding:6px; text-align:center;">{{laItem.CLABORA}}</td>
                        <td style="padding:6px; text-align:center;">{{laItem.DFECHA}}</td>
                        <td style="padding:6px; text-align:left;">{{laItem.CTIPMTO}}</td>
                        <td style="padding:6px; text-align:center;">{{laItem.CTECNIC}}</td>
                        <td style="padding:6px; text-align:left;">{{laItem.CESTADO}}</td>
                     </tr>
                     <!-- Si no hay resultados -->
                     <tr v-if="!paData?.DATOS?.length">
                        <td colspan="4" style="padding:10px; text-align:center;">
                           NO SE ENCONTRARON REGISTROS
                        </td>
                     </tr>
                  </tbody>
               </table>
            </div>
            <!-- Botón Regresar -->
            <div style="margin-top:15px; text-align:right;">
               <Boton3D color="rojo" texto="REGRESAR" style="width:10%;" @click="f_Regresar"></Boton3D>
            </div>
         </div>
         <div v-if="pcScreen === '3'" style="width:100%; height:100vh; display:flex;">
            <div style="width:90%; display:flex; justify-content:center; align-items:flex-start; padding-top:10px;">
            <div style="width:100%; height:80vh; display:flex; justify-content:center; align-items:flex-start;">
               <img v-if="poImage.imageUrl" :src="poImage.imageUrl" style="max-width:95%; max-height:100%; border:1px solid #ccc; border-radius:8px;"/>
            </div>
            </div>
            <div style="width:10%; border-left:1px solid #ddd; display:flex; flex-direction:column; align-items:center; padding-top:20px;">
               <Boton3D color="rojo" texto="VOLVER" style="width:80%;" @click="f_Volver"></Boton3D>
            </div>
         </div>
      </div>
   </div>
</template>

<script setup>
   import LayoutBar from '@/components/LayoutBar.vue'
   import Boton3D from '@/components/Boton3D.vue'
   import Spinner from '@/components/Spinner.vue'
   import {f_Format} from '@/utils/utils'
   import {ref, computed, onMounted} from 'vue'
   import {useRouter} from 'vue-router'

   const plLoading = ref(false)
   const poRouter  = useRouter()
   const paDatos   = ref([])
   const paData    = ref()
   const pcScreen  = ref("1")
   const plError   = ref(false)
   const pcPeriod  = ref('')
   const pcEquipo  = ref('')
   const pcIdEqui  = ref('')
   const poImage   = ref({imageUrl: null});
   const plWorking = ref(false)

   // Init
   onMounted(() => {
      //pcPeriod.value = new Date().getFullYear().toString();
      pcPeriod.value = '2025';
      f_Init();
   })

   async function f_Init() {
      try {
         plLoading.value = true;
         const loRpta = await fetch('http://localhost:8000', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ID: 'DHB0016', CPERIOD: pcPeriod.value})
         })
         if (!loRpta.ok) {
            throw new Error('Error en la respuesta del servidor');
         }
         const laData = await loRpta.json();
         if (laData.ERROR) {
            alert(laData.ERROR);
            poRouter.push({name: 'Mnu1001'});
            return;
         }
         paDatos.value = laData;
      } catch (error) {
         console.error("Error cargando datos:", error);
         alert("ERROR AL CARGAR DATOS");
      } finally {
         plLoading.value = false;
      }
   }

   async function f_Detalle(p_cEquipo) {
      let lcPeriod = pcPeriod.value;
      try {
         plLoading.value = true;
         const loRpta = await fetch('http://localhost:8000/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ID: 'DHB0017', CEQUIPO: p_cEquipo, CPERIOD: lcPeriod})
         })
         if (!loRpta.ok) {
            throw new Error('Error en la respuesta del servidor');
         }
         const laData = await loRpta.json();
         if (laData.ERROR) {
            alert(laData.ERROR);
            poRouter.push({name: 'Mnu1001'});
            return;
         }
         paData.value   = laData;
         pcIdEqui.value = paData.value.ID;
         pcEquipo.value = paData.value.CEQUIPO;
         pcScreen.value = '2';
      } catch (error) {
         console.error("Error cargando datos:", error);
            alert("ERROR AL CARGAR DATOS");
      } finally {
         plLoading.value = false;
      }
   }

   async function f_Grafico() {
      if (plWorking.value) return;
      plWorking.value = true
      console.log("CLICK", performance.now())
      try {
         plLoading.value = true;
         const loRpta = await fetch('http://localhost:8000/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ID: 'DHB0007', NSERIAL: pnSerial.value})
         })
         if (!loRpta.ok) {
            throw new Error('Error en la respuesta del servidor');
         }
         const blob = await loRpta.blob();
         //console.log("Blob size:", blob.size);
         //console.log("Blob type:", blob.type);
         const url = URL.createObjectURL(blob);
         poImage.value = {imageUrl: url};
         pcScreen.value = '3';
      } catch (error) {
         console.error("Error cargando datos:", error);
         alert(error);
      } finally {
         plLoading.value = false;
         plWorking.value = false
      }
   }

   function f_Regresar() {
      pcScreen.value = "1";
      paData.value   = null;
   }

   function f_Volver() {
      pcScreen.value = "2";
   }

   function f_Salir() {
      poRouter.push('/mnu1001');
   }
</script>
