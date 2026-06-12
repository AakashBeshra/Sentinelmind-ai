export interface APIResponse<T = any> {
  status: 'success' | 'error'
  message: string
  data?: T
  error?: string
  timestamp: string
}

export interface PaginatedResponse<T> {
  items: T[]
  total: number
  page: number
  page_size: number
  total_pages: number
}

export interface ErrorResponse {
  error: string
  detail: string
  status_code: number
  timestamp: string
}