<template>
    <nav class="nav-vertical">
      <div class="nav-container">
        <div 
          v-for="(item, index) in navItems" 
          :key="index" 
          class="nav-item"
          :class="{ active: activeItem === item.id }"
          @click="selectItem(item.id)"
        >
          <div class="nav-icon">
            <i :class="item.icon"></i>
          </div>
          <RouterLink class="nav-label" :to="item.link">
            {{ item.label }}
          </RouterLink>
          <div class="nav-indicator" v-if="activeItem === item.id"></div>
        </div>
      </div>
    </nav>
  </template>
  
  <script setup>
  import { ref, computed, defineProps, defineEmits } from 'vue';
  
  // Definición de props
  const props = defineProps({
    // Permite personalizar los elementos de navegación desde el componente padre
    items: {
      type: Array,
      default: () => []
    },
    
    // Item activo inicial
    initialActive: {
      type: String,
      default: ''
    },
    
    // Posición de la navegación: 'left' o 'right'
    position: {
      type: String,
      default: 'left',
      validator: (value) => ['left', 'right'].includes(value)
    },
    
    // Permite expandir/colapsar el menú en pantallas medianas y pequeñas
    collapsed: {
      type: Boolean,
      default: false
    }
  });
  
  // Definición de emisión de eventos
  const emit = defineEmits(['item-selected']);
  
  // Elementos de navegación predeterminados
  const defaultNavItems = [
    { id: 'home', label: 'Inicio', icon: 'fas fa-home', link:'/Home'},
    { id: 'search', label: 'Buscar', icon: 'fas fa-search' , link:'/404'},
    { id: 'notifications', label: 'Notificaciones', icon: 'fas fa-bell' , link:'/Notifications'},
    { id: 'messages', label: 'Mensajes', icon: 'fas fa-envelope' , link:'/404'},
    { id: 'profile', label: 'Perfil', icon: 'fas fa-user' , link:'/404'},
    { id: 'settings', label: 'Ajustes', icon: 'fas fa-cog' , link:'/404'},
    { id: 'help', label: 'Ayuda', icon: 'fas fa-question-circle' , link:'/404'},
    { id: 'logout', label: 'Salir', icon: 'fas fa-sign-out-alt', link:'/' }
  ];
  
  // Usar los elementos proporcionados o los predeterminados
  const navItems = computed(() => 
    props.items.length > 0 ? props.items : defaultNavItems
  );
  
  // Estado para el elemento activo
  const activeItem = ref(props.initialActive || (navItems.value.length > 0 ? navItems.value[0].id : 'home'));
  
  // Función para seleccionar un elemento
  const selectItem = (id) => {
    activeItem.value = id;
    emit('item-selected', id);
  };
  </script>
  
  <style scoped>
  .nav-vertical {
    position: fixed;
    top: 0;
    height: 100vh;
    background-color: #ffffff;
    box-shadow: 2px 0 10px rgba(0, 0, 0, 0.1);
    z-index: 1000;
    width: 240px;
    transition: all 0.3s ease;
  }
  
  .nav-vertical {
    left: v-bind("position === 'left' ? '0' : 'auto'");
    right: v-bind("position === 'right' ? '0' : 'auto'");
  }
  
  .nav-container {
    display: flex;
    flex-direction: column;
    height: 100%;
    padding: 20px 0;
  }
  
  .nav-item {
    display: flex;
    align-items: center;
    padding: 12px 24px;
    cursor: pointer;
    position: relative;
    color: #666;
    transition: all 0.3s ease;
  }
  
  .nav-item:hover {
    color: #333;
    background-color: #f5f5f5;
  }
  
  .nav-item.active {
    color: #4285f4;
    background-color: #e8f0fe;
  }
  
  .nav-icon {
    font-size: 1.2rem;
    width: 24px;
    text-align: center;
    margin-right: 16px;
  }
  
  .nav-label {
    font-size: 0.95rem;
    font-weight: 500;
    text-decoration: none ;
    color: #00008f;
  }
  
  .nav-indicator {
    position: absolute;
    left: 0;
    top: 0;
    width: 4px;
    height: 100%;
    background-color: #4285f4;
  }
  
  /* Versión colapsada para pantallas medianas */
  @media (max-width: 1024px) {
    .nav-vertical {
      width: v-bind("props.collapsed ? '64px' : '240px'");
    }
    
    .nav-item {
      padding: v-bind("props.collapsed ? '16px 0' : '12px 24px'");
      justify-content: v-bind("props.collapsed ? 'center' : 'flex-start'");
    }
    
    .nav-icon {
      margin-right: v-bind("props.collapsed ? '0' : '16px'");
      font-size: v-bind("props.collapsed ? '1.4rem' : '1.2rem'");
    }
    
    .nav-label {
      display: v-bind("props.collapsed ? 'none' : 'block'");
    }
  }
  
  /* Versión para pantallas pequeñas */
  @media (max-width: 768px) {
    .nav-vertical {
      width: v-bind("props.collapsed ? '0' : '240px'");
      transform: v-bind("props.collapsed ? (position === 'left' ? 'translateX(-100%)' : 'translateX(100%)') : 'translateX(0)'");
    }
    
    .nav-item {
      padding: 12px 24px;
      justify-content: flex-start;
    }
    
    .nav-icon {
      margin-right: 16px;
      font-size: 1.2rem;
    }
    
    .nav-label {
      display: block;
    }
  }
  </style>