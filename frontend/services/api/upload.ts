import apiClient from './client'

export const uploadAPI = {
  uploadFile: (file: File) => {
    const formData = new FormData()
    formData.append('file', file)
    return apiClient.post('/upload/file', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
  },
  
  uploadBatch: (files: File[]) => {
    const formData = new FormData()
    files.forEach(file => formData.append('files', file))
    return apiClient.post('/upload/batch', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
  },
  
  getStatus: (fileId: string) => apiClient.get(`/upload/status/${fileId}`),
}