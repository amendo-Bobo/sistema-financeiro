import api from './api'
import type { LoginCredentials, RegisterData, User } from '../types'

export interface AuthResponse {
  access_token: string
  token_type: string
}

export const authService = {
  async login(credentials: LoginCredentials): Promise<AuthResponse> {
    const formData = new URLSearchParams()
    formData.append('username', credentials.email)
    formData.append('password', credentials.password)
    
    const response = await api.post<AuthResponse>('/auth/login', formData, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      }
    })
    return response.data
  },

  async register(data: RegisterData): Promise<User> {
    const response = await api.post<User>('/auth/register', data)
    return response.data
  },

  async getCurrentUser(): Promise<User> {
    const response = await api.get<User>('/auth/me')
    return response.data
  }
}

export default authService
