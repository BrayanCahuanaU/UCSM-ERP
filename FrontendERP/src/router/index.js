import { createRouter, createWebHistory } from 'vue-router'
import Login from '../views/Login.vue'
import Mnu1001 from '../views/Mnu1001.vue'

const routes = [
  { path: '/', redirect: '/login' },
  { path: '/login', name: 'Login', component: Login },
  { path: '/mnu1001', name: 'Mnu1001', component: Mnu1001 },
  { path: '/:pathMatch(.*)*', redirect: '/login' },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
