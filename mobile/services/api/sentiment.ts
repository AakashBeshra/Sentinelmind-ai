import apiClient from './client'

export const sentimentAPI = {
  analyze: async (text: string, includeEmotions: boolean = true) => {
    const response = await apiClient.post('/sentiment/analyze', {
      text,
      include_emotions: includeEmotions,
    })
    return response.data
  },

  batchAnalyze: async (texts: string[], includeEmotions: boolean = true) => {
    const response = await apiClient.post('/sentiment/batch', {
      texts,
      include_emotions: includeEmotions,
    })
    return response.data
  },
}