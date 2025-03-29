<template>
  <div id="containerPrincipal">
    <div id="container">
      <div style="width: 100%;">
        <h1 style="color:#00008f; text-align: center;">Bienvenido <span style="color: red;"> {{ userName }} </span></h1>
        <hr style="width: 100%; color: #00008f;">
      </div>

      <div id="container">
        <button class="boton-bonito separation" @click="obtenerUbicacion"> Sincronizar Ubicación</button>
      <span v-if="isUbicationGet">Gracias, ya tenemos tu ubicación</span>
        <button class="boton-bonito separation" @click="sincronizarCalendario"> Sincronizar Calendario</button>
        <span v-if="isCalendarGet">Gracias, ya tenemos tus eventos del Calendario</span>
        
        <div class="separation">
          <label for="" class="label-bonito">Descripción: </label>
          <textarea name="description" v-model="description" class="textarea-bonito"></textarea>
          <br>
          <span v-if="isDescriptionSend">Acabamos de enviar tus peticiones, recibirás pronto las <RouterLink style="text-decoration: none; color: #00008f;" to="/Notifications">Notificaciones</RouterLink></span>
        </div>
        
        <button class="boton-bonito separation" @click="SendDescription">Enviar</button>
        </div>
    </div>

    <!--
    <notifications style="position: absolute; top: 0; right: 0;"></notifications>
    -->
    <navigation/>
  </div>
</template>

<script setup>
import axios from 'axios';
import { onMounted, ref } from 'vue';
import notifications from '@/components/notifications.vue';
import navigation from '@/components/navigation.vue';


const latitud =ref("")
const longitud  = ref("")
const precision = ref("")
const calendarData = ref("");
const description = ref("");
const urlMap = ref("");
const isUbicationGet = ref(false);
const isCalendarGet = ref(false);
const isDescriptionSend = ref(false);
const userName = ref("");

onMounted(()=>{
  var user =localStorage.getItem("user");
  userName.value = JSON.parse(user).email;
});


async function SendDescription() {
  var data ={
    descripcion:description.value
  }
  //Endpoint Descripcion
  const endpoint = "http://localhost:8050/api/login";
  try{
   calendarData.value = axios.get(endpoint);
   
  }catch(error){
    console.log(error)
  }
  isDescriptionSend.value=true;
  description.value="";
}

async function sincronizarCalendario(){
  //Endpoint Calendar
  const endpoint = "http://localhost:8050/api/";
  try{
   calendarData.value = axios.get(endpoint);
   isCalendarGet.value=true;
  }catch(error){
    console.log(error)
  }
}

function obtenerUbicacion() {
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(mostrarUbicacion, manejarError);
  } 
}

async function mostrarUbicacion(posicion) {
  latitud.value = posicion.coords.latitude;
  longitud.value = posicion.coords.longitude;
  precision.value = posicion.coords.accuracy;
  urlMap.value = "https://www.google.com/maps?q="+latitud.value+","+longitud.value;
  

  //Endpoin Ubicacion
  var endpoint = "http://localhost:8050/api/";
  isUbicationGet.value= true;
  const data ={
    latitud: latitud.value,
    longitud: longitud.value,
    precision: precision.value
  }
  try{
    var response = await axios.post(endpoint, data)
    isUbicationGet.value= true;

  }catch(error){
    console.log(error)
  }


}

function manejarError(error) {
  switch (error.code) {
    case error.PERMISSION_DENIED:
      alert("El usuario denegó la solicitud de geolocalización.");
      break;
    case error.POSITION_UNAVAILABLE:
      alert("La información de ubicación no está disponible.");
      break;
    case error.TIMEOUT:
      alert("La solicitud de ubicación del usuario ha caducado.");
      break;
    case error.UNKNOWN_ERROR:
      alert("Ocurrió un error desconocido.");
      break;
  }
}

//window.onload = obtenerUbicacion;


</script>

<style scopet>

#containerPrincipal{
  font-family: 'Open Sans', Arial, sans-serif;
}

.notification-container {
    position: relative;
    display: inline-block;
}

.notification-dropdown {
    position: absolute;
    top: 100%;
    right: 0;
    background-color: #f9f9f9;
    min-width: 200px;
    box-shadow: 0px 8px 16px 0px rgba(0,0,0,0.2);
    padding: 12px 16px;
    z-index: 1;
}

.notification-item {
    padding: 8px 0;
    border-bottom: 1px solid #ddd;
}



.separation{
  margin-top: 2rem;
}

#container{
  display: flex;
  flex-direction: column;
  align-items: center;
  padding-top: 1rem;
  padding-bottom:1rem;
}

.label-bonito {
  display: block; /* Para que ocupen todo el ancho disponible y tengan margen vertical */
  margin-bottom: 5px; /* Espacio entre la etiqueta y el input */
  font-size: 14px;
  color: #00008f; /* Color de texto oscuro para legibilidad */
  font-weight: 600; /* Peso de la fuente ligeramente más grueso para destacar */
}

/* Opcional: Estilo para labels requeridos */
.label-bonito.requerido::after {
  content: "*"; /* Agrega un asterisco para indicar que es requerido */
  color: red;
  margin-left: 3px;
}
.textarea-bonito {
  padding: 12px 15px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 16px;
  width: 100%; /* Ocupa todo el ancho disponible */
  max-width: 500px; /* Ancho máximo para evitar que se extienda demasiado */
  box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: border-color 0.3s ease;
  resize: vertical; /* Permite redimensionar verticalmente */
}

.textarea-bonito:focus {
  border-color: #00008f;
  outline: none;
  box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.2);
}

.textarea-bonito::placeholder {
  color: #aaa;
}


.boton-bonito {
  background: #00008f; /* Degradado de azul */
  color: white;
  padding: 15px 30px;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  cursor: pointer;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2); /* Sombra suave */
  transition: all 0.3s ease; /* Transición suave para efectos hover */
}

.boton-bonito:hover {
  background: #5656c2; /* Invierte el degradado al pasar el ratón */
  transform: translateY(-2px); /* Ligero efecto de elevación al pasar el ratón */
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.3); /* Sombra más pronunciada al pasar el ratón */
}
.boton-bonito:active {
  transform: translateY(1px); /* Ligero efecto de presión al hacer clic */
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2); /* Sombra más sutil al hacer clic */
}


.textarea-bonito {
  padding: 12px 15px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 16px;
  width: 100%; /* Ocupa todo el ancho disponible */
  max-width: 500px; /* Ancho máximo para evitar que se extienda demasiado */
  box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: border-color 0.3s ease;
  resize: vertical; /* Permite redimensionar verticalmente */
}

.textarea-bonito:focus {
  border-color: #00008f;
  outline: none;
  box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.2);
}

.textarea-bonito::placeholder {
  color: #aaa;
}








</style>
