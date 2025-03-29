<template>
  <div class="notifications-container">
    <div style="width: 100%">
      <h1 style="color: #00008f; text-align: center">
        Bienvenido <span style="color: red"> {{ userName }} </span>
      </h1>
      <hr style="width: 100%; color: #00008f" />
    </div>
    <div class="notifications-header">
      <h3>Notificaciones</h3>
      <button @click="markAllAsRead" class="btn-read-all">
        Marcar todas como leídas
      </button>
    </div>

    <div class="notifications-list">
      <div
        v-for="(notification, index) in notifications"
        :key="notification.id"
        class="notification-item"
        :class="{
          unread: !notification.read,
          expanded: expandedNotification === index,
        }"
        @click="toggleExpand(index)"
      >
        <div class="notification-dot" v-if="!notification.read"></div>
        <div class="notification-content">
          <div class="notification-header">
            <div class="notification-title">{{ notification.title }}</div>
            <div class="notification-time">
              {{ formatTime(notification.time) }}
            </div>
          </div>
          <div class="notification-description" v-if="!isExpanded(index)">
            <p v-html="formatDescription(notification.description)"></p>
          </div>
          <div class="notification-full" v-if="isExpanded(index)">
            <p>{{ notification.description }}</p>
            <div class="notification-actions">
              <button
                @click.stop="markAsRead(notification.id)"
                v-if="!notification.read"
                class="btn-action"
              >
                Marcar como leída
              </button>
              <button
                @click.stop="deleteNotification(notification.id)"
                class="btn-action btn-delete"
              >
                Eliminar
              </button>
            </div>
          </div>
        </div>
      </div>

      <div v-if="notifications.length === 0" class="no-notifications">
        No tienes notificaciones nuevas.
      </div>
    </div>
    <navigation />
  </div>
</template>
<script setup>
import { ref, computed, onMounted } from "vue";
import navigation from "@/components/navigation.vue";
// Estado reactivo
const userName = ref("");

onMounted(() => {
  var user = localStorage.getItem("user");
  userName.value = JSON.parse(user).email;
});

const expandedNotification = ref(null);

const notifications = ref([]);

const formatDescription = (text) => {
  return text.replace(/\n/g, "<br>");
};

onMounted(() => {
  const storedNotifications = JSON.parse(
    localStorage.getItem("Notifications")
  ) || { data: { response: "" } };
  notifications.value = [
    {
      id: 1,
      title: "Sugerencia de viaje",
      description: storedNotifications.data.response, // Corrección aquí
      time: new Date(Date.now() - 1000 * 60 * 30), // 30 minutos atrás
      read: false,
    },
  ];
});

// Métodos
const isExpanded = (index) => {
  return expandedNotification.value === index;
};

const toggleExpand = (index) => {
  if (expandedNotification.value === index) {
    expandedNotification.value = null;
  } else {
    expandedNotification.value = index;
    // Marcar como leída al expandir
    if (!notifications.value[index].read) {
      notifications.value[index].read = true;
    }
  }
};

const truncateText = (text) => {
  return text.length > 50 ? text.substring(0, 50) + "..." : text;
};

const formatTime = (time) => {
  const now = new Date();
  const diffMs = now - time;
  const diffMin = Math.floor(diffMs / (1000 * 60));
  const diffHours = Math.floor(diffMs / (1000 * 60 * 60));
  const diffDays = Math.floor(diffMs / (1000 * 60 * 60 * 24));

  if (diffMin < 60) {
    return `Hace ${diffMin} min`;
  } else if (diffHours < 24) {
    return `Hace ${diffHours} h`;
  } else {
    return `Hace ${diffDays} d`;
  }
};

const markAsRead = (id) => {
  const notification = notifications.value.find((n) => n.id === id);
  if (notification) {
    notification.read = true;
  }
};

const markAllAsRead = () => {
  notifications.value.forEach((notification) => {
    notification.read = true;
  });
};

const deleteNotification = (id) => {
  expandedNotification.value = null;
  notifications.value = notifications.value.filter((n) => n.id !== id);
};
</script>

<style scoped>
.notifications-container {
  width: 100%;
  max-width: 600px;
  margin: 0 auto;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  font-family: Arial, sans-serif;
}

.notifications-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 16px;
  border-bottom: 1px solid #e0e0e0;
}

.notifications-header h3 {
  margin: 0;
  font-size: 16px;
  color: #202124;
}

.btn-read-all {
  background: none;
  border: none;
  color: #1a73e8;
  font-size: 14px;
  cursor: pointer;
  padding: 4px 8px;
  border-radius: 4px;
}

.btn-read-all:hover {
  background-color: rgba(26, 115, 232, 0.1);
}

.notifications-list {
  max-height: 400px;
  overflow-y: auto;
}

.notification-item {
  position: relative;
  padding: 12px 16px;
  border-bottom: 1px solid #e0e0e0;
  cursor: pointer;
  display: flex;
  transition: background-color 0.2s;
}

.notification-item:hover {
  background-color: #f5f5f5;
}

.notification-item.unread {
  background-color: #f2f6fc;
}

.notification-item.expanded {
  background-color: #f2f6fc;
}

.notification-dot {
  width: 8px;
  height: 8px;
  background-color: #1a73e8;
  border-radius: 50%;
  position: absolute;
  left: 6px;
  top: 18px;
}

.notification-content {
  flex: 1;
  margin-left: 14px;
}

.notification-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 4px;
}

.notification-title {
  font-weight: bold;
  color: #00008f;
  font-size: 14px;
}

.notification-time {
  color: #5f6368;
  font-size: 12px;
}

.notification-description {
  color: #5f6368;
  font-size: 14px;
  line-height: 1.4;
}

.notification-full {
  color: #202124;
  font-size: 14px;
  line-height: 1.4;
  margin-top: 8px;
}

.notification-actions {
  display: flex;
  justify-content: flex-end;
  margin-top: 12px;
  gap: 8px;
}

.btn-action {
  background: none;
  border: 1px solid #dadce0;
  border-radius: 4px;
  padding: 6px 12px;
  font-size: 13px;
  cursor: pointer;
  color: #1a73e8;
}

.btn-action:hover {
  background-color: rgba(26, 115, 232, 0.1);
}

.btn-delete {
  color: #ea4335;
}

.btn-delete:hover {
  background-color: rgba(234, 67, 53, 0.1);
}

.no-notifications {
  padding: 24px 16px;
  text-align: center;
  color: #5f6368;
  font-size: 14px;
}
</style>
