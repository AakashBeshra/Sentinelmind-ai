import apiClient from './client'

export const analyticsAPI = {
  getDashboardStats: (days?: number) =>
    apiClient.get('/analytics/dashboard', { params: { days } }),
  
  getTrends: (start_date?: string, end_date?: string, interval?: string) =>
    apiClient.get('/analytics/trends', { params: { start_date, end_date, interval } }),
  
  getEmotionDistribution: (days?: number) =>
    apiClient.get('/analytics/emotion-distribution', { params: { days } }),
  
  getTopKeywords: (limit?: number, days?: number) =>
    apiClient.get('/analytics/top-keywords', { params: { limit, days } }),
  
  exportData: (data: { start_date: string; end_date: string; format: string }) =>
    apiClient.post('/analytics/export', data),
}