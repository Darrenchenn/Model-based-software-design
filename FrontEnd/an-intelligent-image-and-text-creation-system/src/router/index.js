import { createRouter, createWebHistory } from 'vue-router'
import LoginView from '../views/loginView.vue'
import HomeView from '../views/homeView.vue'
import IndexView from '../views/indexView.vue'

const isAuthentication = () => {
  // return false
  if (localStorage.getItem('userName') === null) return false
  else return true
}

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'Index',
      component: IndexView,
      beforeEnter: (to, from) => {
        if (isAuthentication()) return { name: 'Home' }
      }
    },
    {
      path: '/login',
      name: 'Login',
      component: LoginView,
      beforeEnter: (to, from) => {
        if (isAuthentication()) return { name: 'Home' }
      }
    },
    {
      path: '/home',
      name: 'Home',
      component: HomeView
    }
  ]
})

router.beforeEach(async (to, _) => {
  if (!isAuthentication() && to.name !== 'Login') {
    return { name: 'Login' }
  }
})

export default router
