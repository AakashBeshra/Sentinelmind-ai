import apiClient from './client'

export const sentimentAPI = {
  analyze: (data: { text: string; include_emotions?: boolean; include_toxicity?: boolean }) =>
    apiClient.post('/sentiment/analyze', data),
  
  batchAnalyze: (data: { texts: string[]; include_emotions?: boolean }) =>
    apiClient.post('/sentiment/batch', data),
  
  getLanguages: () => apiClient.get('/sentiment/languages'),
}