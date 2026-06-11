import { create } from 'zustand'
import { secureStorage } from '../services/storage/secureStorage'

interface User {
  id: number
  email: string
  username: string
  full_name: string
  role: string
  is_premium: boolean
}

interface AuthState {
  user: User | null
  isAuthenticated: boolean
  isLoading: boolean
  login: (email: string, password: string) => Promise<void>
  logout: () => void
  setUser: (user: User) => void
}

export const useAuthStore = create<AuthState>((set) => ({
  user: null,
  isAuthenticated: false,
  isLoading: false,

  login: async (email: string, password: string) => {
    set({ isLoading: true })
    try {
      // API call here
      const response = await fetch('http://localhost:8000/api/v1/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password }),
      })
      const data = await response.json()
      
      await secureStorage.setToken(data.access_token)
      set({ user: data.user, isAuthenticated: true, isLoading: false })
    } catch (error) {
      set({ isLoading: false })
      throw error
    }
  },

  logout: () => {
    secureStorage.removeToken()
    set({ user: null, isAuthenticated: false })
  },

  setUser: (user) => set({ user }),
}))