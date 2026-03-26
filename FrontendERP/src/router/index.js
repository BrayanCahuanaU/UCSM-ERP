import { createRouter, createWebHistory } from 'vue-router'
import Login   from '../components/Login.vue'
import Dhb1140 from '../components/Dhb1140.vue'
import Tes1100 from '../components/Tes1100.vue'
import Tes1110 from '../components/Tes1110.vue'

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/',
    name: 'home',
    component: Dhb1140
  },
  {
    path: '/dhb1140',
    name: 'Dhb1140',
    component: Dhb1140
  },
  {
    path: '/tes1100',
    name: 'Tes1100',
    component: Tes1100
  },
  {
    path: '/tes1110',
    name: 'Tes1110',
    component: Tes1110
  },
  {
    path: '/tes1120',
    name: 'Tes1120',
    component: Tes1110  // Temporal: usa el mismo componente de PDT
  }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

export default router