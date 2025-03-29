<template>
    <div class="notificaciones-container">
      <!-- Botón de notificaciones con contador -->
      <button class="btn-notificaciones" @click="toggleNotificaciones">
        <span class="icono-notificacion">🔔</span>
        <span v-if="notificacionesSinLeer > 0" class="contador-notificaciones">
          {{ notificacionesSinLeer }}
        </span>
      </button>
  
      <!-- Panel desplegable de notificaciones -->
      <div v-if="mostrarNotificaciones" class="panel-notificaciones">
        <div class="header-notificaciones">
          <h3>Notificaciones</h3>
          <button v-if="tieneNotificacionesSinLeer" 
                  @click="marcarTodasComoLeidas" 
                  class="btn-marcar-leidas">
            Marcar todas como leídas
          </button>
        </div>
  
        <div v-if="notificaciones.length === 0" class="sin-notificaciones">
          No tienes notificaciones
        </div>
  
        <ul v-else class="lista-notificaciones">
          <li v-for="(notificacion, index) in notificaciones" 
              :key="index" 
              class="item-notificacion"
              :class="{ 'no-leida': !notificacion.leida }"
              @click="marcarComoLeida(index)">
            <div class="contenido-notificacion">
              <h4 class="titulo-notificacion">{{ notificacion.titulo }}</h4>
              <p class="descripcion-notificacion">{{ notificacion.descripcion }}</p>
              <span class="fecha-notificacion">{{ formatearFecha(notificacion.fecha) }}</span>
            </div>
          </li>
        </ul>
      </div>
    </div>
  </template>
  
  <script>
  import { ref, computed } from 'vue';
  
  export default {
    name: 'NotificacionesDropdown',
    
    props: {
      // Puedes recibir las notificaciones como prop desde el componente padre
      notificacionesIniciales: {
        type: Array,
        default: () => []
      }
    },
    
    setup(props) {
      // Estado de las notificaciones
      const notificaciones = ref(props.notificacionesIniciales.length > 0 
        ? props.notificacionesIniciales 
        : [
          {
            titulo: 'Nueva actualización',
            descripcion: 'Se ha lanzado una nueva versión del sistema',
            fecha: new Date(),
            leida: false
          },
          {
            titulo: 'Recordatorio',
            descripcion: 'Tienes una reunión pendiente para mañana',
            fecha: new Date(Date.now() - 3600000), // 1 hora atrás
            leida: false
          },
          {
            titulo: 'Mensaje del sistema',
            descripcion: 'Tu cuenta ha sido verificada correctamente',
            fecha: new Date(Date.now() - 86400000), // 1 día atrás
            leida: true
          }
        ]);
      
      // Estado del desplegable
      const mostrarNotificaciones = ref(false);
      
      // Computar número de notificaciones sin leer
      const notificacionesSinLeer = computed(() => {
        return notificaciones.value.filter(n => !n.leida).length;
      });
      
      const tieneNotificacionesSinLeer = computed(() => {
        return notificacionesSinLeer.value > 0;
      });
      
      // Abrir/cerrar el panel de notificaciones
      const toggleNotificaciones = () => {
        mostrarNotificaciones.value = !mostrarNotificaciones.value;
      };
      
      // Marcar una notificación como leída
      const marcarComoLeida = (index) => {
        notificaciones.value[index].leida = true;
      };
      
      // Marcar todas las notificaciones como leídas
      const marcarTodasComoLeidas = () => {
        notificaciones.value.forEach(notificacion => {
          notificacion.leida = true;
        });
      };
      
      // Formatear la fecha de la notificación
      const formatearFecha = (fecha) => {
        const ahora = new Date();
        const diff = ahora - new Date(fecha);
        
        // Menos de 1 minuto
        if (diff < 60000) {
          return 'Ahora mismo';
        }
        
        // Menos de 1 hora
        if (diff < 3600000) {
          const minutos = Math.floor(diff / 60000);
          return `Hace ${minutos} ${minutos === 1 ? 'minuto' : 'minutos'}`;
        }
        
        // Menos de 1 día
        if (diff < 86400000) {
          const horas = Math.floor(diff / 3600000);
          return `Hace ${horas} ${horas === 1 ? 'hora' : 'horas'}`;
        }
        
        // Menos de 7 días
        if (diff < 604800000) {
          const dias = Math.floor(diff / 86400000);
          return `Hace ${dias} ${dias === 1 ? 'día' : 'días'}`;
        }
        
        // Fecha normal
        return fecha.toLocaleDateString();
      };
      
      return {
        notificaciones,
        mostrarNotificaciones,
        notificacionesSinLeer,
        tieneNotificacionesSinLeer,
        toggleNotificaciones,
        marcarComoLeida,
        marcarTodasComoLeidas,
        formatearFecha
      };
    }
  };
  </script>
  
  <style scoped>
  .notificaciones-container {
    position: relative;
    display: inline-block;
  }
  
  .btn-notificaciones {
    background: none;
    border: none;
    cursor: pointer;
    position: relative;
    font-size: 1.5rem;
    padding: 0.5rem;
  }
  
  .contador-notificaciones {
    position: absolute;
    top: 0;
    right: 0;
    background-color: #ff4757;
    color: white;
    border-radius: 50%;
    font-size: 0.7rem;
    width: 1.2rem;
    height: 1.2rem;
    display: flex;
    align-items: center;
    justify-content: center;
  }
  
  .panel-notificaciones {
    position: absolute;
    top: 100%;
    right: 0;
    width: 320px;
    max-height: 400px;
    overflow-y: auto;
    background-color: white;
    border-radius: 4px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    z-index: 1000;
  }
  
  .header-notificaciones {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.8rem 1rem;
    border-bottom: 1px solid #eee;
  }
  
  .header-notificaciones h3 {
    margin: 0;
    font-size: 1rem;
  }
  
  .btn-marcar-leidas {
    background: none;
    border: none;
    font-size: 0.8rem;
    color: #2196f3;
    cursor: pointer;
  }
  
  .sin-notificaciones {
    padding: 2rem 1rem;
    text-align: center;
    color: #777;
  }
  
  .lista-notificaciones {
    list-style: none;
    margin: 0;
    padding: 0;
  }
  
  .item-notificacion {
    padding: 1rem;
    border-bottom: 1px solid #eee;
    cursor: pointer;
    transition: background-color 0.2s;
  }
  
  .item-notificacion:hover {
    background-color: #f9f9f9;
  }
  
  .item-notificacion.no-leida {
    background-color: #f5f9ff;
  }
  
  .item-notificacion.no-leida::before {
    content: '';
    display: block;
    width: 8px;
    height: 8px;
    background-color: #2196f3;
    border-radius: 50%;
    position: absolute;
    left: 8px;
    margin-top: 6px;
  }
  
  .contenido-notificacion {
    margin-left: 16px;
  }
  
  .titulo-notificacion {
    margin: 0 0 0.3rem;
    font-size: 0.95rem;
    font-weight: 600;
    color: #00008f;
  }
  
  .descripcion-notificacion {
    margin: 0 0 0.5rem;
    font-size: 0.85rem;
  }
  
  .fecha-notificacion {
    font-size: 0.75rem;
    color: #999;
  }
  </style>