import { createRouter, createWebHistory } from 'vue-router'
import LoginView from '../views/loginView.vue'
import HomeView from '../views/homeView.vue'
import IndexView from '../views/indexView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'Index',
      component: IndexView
    },
    {
      path: '/login',
      name: 'Login',
      component: LoginView
    },
    {
      path: '/home',
      name: 'Home',
      component: HomeView
    }
  ]
})

export default router
