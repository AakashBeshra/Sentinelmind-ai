export interface User {
  id: number
  email: string
  username: string
  full_name: string
  role: 'user' | 'premium' | 'admin' | 'super_admin'
  is_active: boolean
  is_verified: boolean
  is_premium: boolean
  total_analyses: number
  created_at: string
}

export interface UserProfile extends User {
  api_calls_limit: number
  api_calls_used: number
  premium_until: string | null
  last_active: string
}

export interface LoginRequest {
  email: string
  password: string
}

export interface RegisterRequest {
  email: string
  username: string
  password: string
  full_name?: string
}

export interface AuthResponse {
  access_token: string
  refresh_token: string
  token_type: string
}