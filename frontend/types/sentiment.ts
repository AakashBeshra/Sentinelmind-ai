export interface SentimentRequest {
  text: string
  language?: string
  include_emotions?: boolean
  include_toxicity?: boolean
  include_entities?: boolean
}

export interface SentimentResponse {
  sentiment: 'positive' | 'negative' | 'neutral'
  confidence: number
  probabilities: {
    positive: number
    negative: number
    neutral: number
  }
  emotions?: Record<string, number>
  toxicity?: {
    is_toxic: boolean
    confidence: number
  }
  entities?: Array<{
    text: string
    label: string
  }>
  language: string
  processing_time_ms: number
  timestamp: string
}

export interface BatchSentimentRequest {
  texts: string[]
  language?: string
  include_emotions?: boolean
}

export interface BatchSentimentResponse {
  results: SentimentResponse[]
  batch_id: string
  total_processing_time_ms: number
  successful_count: number
  failed_count: number
}