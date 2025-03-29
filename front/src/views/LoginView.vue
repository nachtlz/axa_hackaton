<template>
  <div id="container">
    <img src="@/assets/logo.svg" alt="" />
    <div class="child-container">
      <label class="label-bonito" for="email">Email: </label>
      <input class="input-bonito" type="email" v-model="email" />
    </div>

    <div class="child-container">
      <label class="label-bonito" for="email">Contraseña: </label>
      <input class="input-bonito" type="password" v-model="password" />
    </div>

    <button @click="checkUser()" class="child-container boton-bonito">
      Entrar
    </button>
  </div>
</template>

<script setup>
import router from "@/router";
import axios from "axios";
import { ref } from "vue";
import { RouterLink } from "vue-router";
const email = ref("");
const password = ref("");

async function checkUser() {
  var data = {
    email: email.value,
  };
  localStorage.setItem("user", JSON.stringify(data));
  var endpoint = "http://localhost:8050/api/recommendations";
  try {
    var response = await axios.post(endpoint, data);

    localStorage.setItem("Notifications", JSON.stringify(response));
  } catch (error) {
    console.log(error);
  }

  router.push("/Home");
}
</script>

<style scoped>
#container {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding-top: 6rem;
  font-family: "Open Sans", Arial, sans-serif;
}

.child-container {
  margin-top: 1rem;
}

.input-bonito {
  padding: 12px 15px;
  border: 1px solid #ddd; /* Borde gris claro */
  border-radius: 6px;
  font-size: 16px;
  width: 300px; /* Ancho fijo, ajusta según necesites */
  box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.1); /* Sombra interna sutil */
  transition: border-color 0.3s ease; /* Transición suave para el cambio de color del borde */
}

.input-bonito:focus {
  border-color: #00008f; /* Borde azul al enfocar */
  outline: none; /* Elimina el borde de enfoque predeterminado del navegador */
  box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.2); /* Sombra interna ligeramente más pronunciada al enfocar */
}

/* Estilo para placeholders */
.input-bonito::placeholder {
  color: #aaa;
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
  transform: translateY(
    -2px
  ); /* Ligero efecto de elevación al pasar el ratón */
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.3); /* Sombra más pronunciada al pasar el ratón */
}

.boton-bonito:active {
  transform: translateY(1px); /* Ligero efecto de presión al hacer clic */
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2); /* Sombra más sutil al hacer clic */
}
</style>
