export interface EmotionRequest {
  text: string
  language?: string
}

export interface EmotionResponse {
  dominant_emotion: string
  dominant_confidence: number
  all_emotions: Record<string, number>
  intensity: 'low' | 'medium' | 'high'
  recommendation?: string
}

export interface EmotionTimeline {
  timestamp: string
  emotion: string
  confidence: number
  intensity: string
}