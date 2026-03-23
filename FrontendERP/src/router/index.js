import { createRouter, createWebHistory } from 'vue-router'
import Dhb1140 from '../components/Dhb1140.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: Dhb1140
  }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

export default router