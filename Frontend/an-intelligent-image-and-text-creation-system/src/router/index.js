import { createRouter, createWebHistory } from 'vue-router'
import { isAuthenticate } from '../script/helperFunction.js'
import LoginView from '../views/loginView.vue'
import HomeView from '../views/homeView.vue'
import ContentCreate from '../views/creator_contentCreateView.vue'
import ViewCreateHistory from '../views/creator_HistoryView.vue'
import CreateHistoryDetail from '../views/creator_HistoryDetailView.vue'
import AccountView from '../views/accountView.vue'
import IndexView from '../views/indexView.vue'
import AuditionView from '../views/supervisor_auditionView.vue'
import AuditionHistoryView from '../views/supervisor_auditionHistoryView.vue'
import TemplateView from '../views/supervisor_templateView.vue'

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
      path: '/view_create_history/:id',
      component: CreateHistoryDetail
    },
    {
      path: '/account',
      name: 'Account',
      component: AccountView
    },
    {
      path: '/audition',
      name: 'Audition',
      component: AuditionView
    },
    {
      path: '/audition_history',
      name: 'View Audition History',
      component: AuditionHistoryView
    },
    {
      path: '/create_template',
      name: 'Create Template',
      component: TemplateView
    }
  ]
})

router.beforeEach(async (to, _) => {
  if (!isAuthenticate() && to.name !== 'Login') {
    return { name: 'Login' }
  }
})

export default router
