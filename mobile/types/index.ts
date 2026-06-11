export interface User {
  id: number
  email: string
  username: string
  full_name: string
  role: 'user' | 'premium' | 'admin'
  is_premium: boolean
}

export interface SentimentResult {
  sentiment: 'positive' | 'negative' | 'neutral'
  confidence: number
  probabilities: {
    positive: number
    negative: number
    neutral: number
  }
  emotions?: Record<string, number>
  processing_time_ms: number
}

export interface EmotionResult {
  dominant_emotion: string
  dominant_confidence: number
  all_emotions: Record<string, number>
  intensity: 'low' | 'medium' | 'high'
}

export interface AnalysisHistory {
  id: string
  text: string
  sentiment: string
  confidence: number
  created_at: string
}