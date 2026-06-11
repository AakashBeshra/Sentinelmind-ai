export const API_BASE_URL = 'http://localhost:8000/api/v1'
export const WS_BASE_URL = 'ws://localhost:8000'

export const SENTIMENT_LABELS = {
  POSITIVE: 'positive',
  NEGATIVE: 'negative',
  NEUTRAL: 'neutral',
} as const

export const EMOTION_LABELS = {
  JOY: 'joy',
  SADNESS: 'sadness',
  ANGER: 'anger',
  FEAR: 'fear',
  LOVE: 'love',
  SURPRISE: 'surprise',
} as const

export const STORAGE_KEYS = {
  TOKEN: 'access_token',
  REFRESH_TOKEN: 'refresh_token',
  USER: 'user',
  THEME: 'theme',
}

export const ROUTES = {
  LOGIN: '/login',
  REGISTER: '/register',
  HOME: '/(tabs)',
  ANALYTICS: '/(tabs)/analytics',
  PROFILE: '/(tabs)/profile',
  OCR: '/camera/ocr',
  VOICE: '/voice/recorder',
}