import { createContext, useContext, useState, useEffect, ReactNode } from 'react'
import { authService } from '../services/auth'
import type { User, LoginCredentials, RegisterData } from '../types'

interface AuthContextType {
  user: User | null
  isAuthenticated: boolean
  isLoading: boolean
  login: (credentials: LoginCredentials) => Promise<void>
  register: (data: RegisterData) => Promise<void>
  logout: () => void
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null)
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    const token = localStorage.getItem('token')
    if (token) {
      authService.getCurrentUser()
        .then(user => setUser(user))
        .catch(() => localStorage.removeItem('token'))
        .finally(() => setIsLoading(false))
    } else {
      setIsLoading(false)
    }
  }, [])

  const login = async (credentials: LoginCredentials) => {
    const response = await authService.login(credentials)
    localStorage.setItem('token', response.access_token)
    const user = await authService.getCurrentUser()
    setUser(user)
  }

  const register = async (data: RegisterData) => {
    await authService.register(data)
  }

  const logout = () => {
    localStorage.removeItem('token')
    setUser(null)
  }

  return (
    <AuthContext.Provider value={{
      user,
      isAuthenticated: !!user,
      isLoading,
      login,
      register,
      logout
    }}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
}
