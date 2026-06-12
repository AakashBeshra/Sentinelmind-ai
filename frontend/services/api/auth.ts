import apiClient from './client'

export const authAPI = {
  register: (data: { email: string; username: string; password: string; full_name?: string }) =>
    apiClient.post('/auth/register', data),
  
  login: (data: { email: string; password: string }) =>
    apiClient.post('/auth/login', data),
  
  logout: () => apiClient.post('/auth/logout'),
  
  refreshToken: (refresh_token: string) =>
    apiClient.post('/auth/refresh', { refresh_token }),
  
  changePassword: (old_password: string, new_password: string) =>
    apiClient.post('/auth/change-password', { old_password, new_password }),
}