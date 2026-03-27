/** 认证状态管理 */
import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { User } from '../types'
import { loginApi, registerApi, getMeApi } from '../api/auth'

export const useAuthStore = defineStore('auth', () => {
  const user = ref<User | null>(null)
  const token = ref(localStorage.getItem('token') || '')

  const isLoggedIn = () => !!token.value

  async function login(username: string, password: string) {
    const { data } = await loginApi(username, password)
    token.value = data.access_token
    user.value = data.user
    localStorage.setItem('token', data.access_token)
  }

  async function register(username: string, password: string) {
    const { data } = await registerApi(username, password)
    token.value = data.access_token
    user.value = data.user
    localStorage.setItem('token', data.access_token)
  }

  async function fetchUser() {
    try {
      const { data } = await getMeApi()
      user.value = data
    } catch {
      logout()
    }
  }

  function logout() {
    token.value = ''
    user.value = null
    localStorage.removeItem('token')
  }

  return { user, token, isLoggedIn, login, register, fetchUser, logout }
})
