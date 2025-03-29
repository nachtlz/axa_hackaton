import { createRouter, createWebHistory } from 'vue-router'
import LoginView from '@/views/LoginView.vue'
import PrincipalView from '@/views/PrincipalView.vue'
import NotificationView from '@/views/NotificationView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'login',
      component: LoginView,
    },
    {
      path: '/Home',
      name: 'Home',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: PrincipalView,
    },
    {
      path: '/Notifications',
      name: 'Notifications',
      component: NotificationView,
    },
  ],
})

export default router
