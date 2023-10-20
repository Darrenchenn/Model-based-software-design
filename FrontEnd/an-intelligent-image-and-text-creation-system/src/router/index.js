import { createRouter, createWebHistory } from 'vue-router'
import { isAuthenticate } from '../script/helperFunction.js'
import LoginView from '../views/loginView.vue'
import HomeView from '../views/homeView.vue'
import ContentCreate from '../views/contentCreateView.vue'
import ViewCreateHistory from '../views/creatorHistoryView.vue'
import AccountView from '../views/accountView.vue'
import IndexView from '../views/indexView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'Index',
      component: IndexView,
      beforeEnter: (to, from) => {
        if (isAuthenticate()) return { name: 'Home' }
      }
    },
    {
      path: '/login',
      name: 'Login',
      meta: { hideNavBar: true },
      component: LoginView,
      beforeEnter: (to, from) => {
        if (isAuthenticate()) return { name: 'Home' }
      }
    },
    {
      path: '/home',
      name: 'Home',
      component: HomeView
    },
    {
      path: '/content_create',
      name: 'Content Create',
      component: ContentCreate
    },
    {
      path: '/view_create_history',
      name: 'View Create History',
      component: ViewCreateHistory
    },
    {
      path: '/account',
      name: 'Account',
      component: AccountView
    }
  ]
})

router.beforeEach(async (to, _) => {
  if (!isAuthenticate() && to.name !== 'Login') {
    return { name: 'Login' }
  }
})

export default router
