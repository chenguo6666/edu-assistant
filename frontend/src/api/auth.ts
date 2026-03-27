/** 认证相关 API */
import api from './index'
import type { TokenResponse, User } from '../types'

export function registerApi(username: string, password: string) {
  return api.post<TokenResponse>('/auth/register', { username, password })
}

export function loginApi(username: string, password: string) {
  return api.post<TokenResponse>('/auth/login', { username, password })
}

export function getMeApi() {
  return api.get<User>('/auth/me')
}
