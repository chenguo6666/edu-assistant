import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/login',
      name: 'Login',
      component: () => import('../views/LoginView.vue'),
    },
    {
      path: '/register',
      name: 'Register',
      component: () => import('../views/RegisterView.vue'),
    },
    {
      path: '/',
      name: 'Chat',
      component: () => import('../views/ChatView.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/profile',
      name: 'Profile',
      component: () => import('../views/UserProfileView.vue'),
      meta: { requiresAuth: true },
    },
  ],
})

// 路由守卫：未登录跳转到登录页
router.beforeEach((to) => {
  const token = localStorage.getItem('token')
  if (to.meta.requiresAuth && !token) {
    return { name: 'Login' }
  }
})

export default router
