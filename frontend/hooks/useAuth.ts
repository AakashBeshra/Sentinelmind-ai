import { create } from 'zustand'
import { persist } from 'zustand/middleware'
import axios from 'axios'
import toast from 'react-hot-toast'

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
  token: string | null
  isLoading: boolean
  login: (email: string, password: string) => Promise<void>
  register: (data: any) => Promise<void>
  logout: () => void
  updateUser: (user: User) => void
}

export const useAuth = create<AuthState>()(
  persist(
    (set) => ({
      user: null,
      token: null,
      isLoading: false,

      login: async (email: string, password: string) => {
        set({ isLoading: true })
        try {
          const response = await axios.post('/api/auth/login', { email, password })
          const { access_token, refresh_token } = response.data
          
          // Store tokens
          localStorage.setItem('access_token', access_token)
          localStorage.setItem('refresh_token', refresh_token)
          
          // Get user profile
          const userResponse = await axios.get('/api/users/me', {
            headers: { Authorization: `Bearer ${access_token}` }
          })
          
          set({ user: userResponse.data, token: access_token, isLoading: false })
          toast.success('Login successful!')
        } catch (error: any) {
          set({ isLoading: false })
          toast.error(error.response?.data?.detail || 'Login failed')
          throw error
        }
      },

      register: async (userData) => {
        set({ isLoading: true })
        try {
          await axios.post('/api/auth/register', userData)
          toast.success('Registration successful! Please login.')
          set({ isLoading: false })
        } catch (error: any) {
          set({ isLoading: false })
          toast.error(error.response?.data?.detail || 'Registration failed')
          throw error
        }
      },

      logout: () => {
        localStorage.removeItem('access_token')
        localStorage.removeItem('refresh_token')
        set({ user: null, token: null })
        toast.success('Logged out successfully')
      },

      updateUser: (user) => set({ user })
    }),
    {
      name: 'auth-storage',
      getStorage: () => localStorage
    }
  )
)