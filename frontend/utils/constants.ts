export const API_ENDPOINTS = {
  AUTH: {
    LOGIN: '/auth/login',
    REGISTER: '/auth/register',
    LOGOUT: '/auth/logout',
    REFRESH: '/auth/refresh',
    CHANGE_PASSWORD: '/auth/change-password',
  },
  SENTIMENT: {
    ANALYZE: '/sentiment/analyze',
    BATCH: '/sentiment/batch',
    LANGUAGES: '/sentiment/languages',
  },
  EMOTION: {
    DETECT: '/emotion/detect',
    LIST: '/emotion/list',
  },
  ANALYTICS: {
    DASHBOARD: '/analytics/dashboard',
    TRENDS: '/analytics/trends',
    EMOTIONS: '/analytics/emotion-distribution',
    KEYWORDS: '/analytics/top-keywords',
    EXPORT: '/analytics/export',
  },
  UPLOAD: {
    FILE: '/upload/file',
    BATCH: '/upload/batch',
    STATUS: '/upload/status',
  },
}

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

export const RATE_LIMITS = {
  FREE: {
    REQUESTS_PER_MINUTE: 10,
    BATCH_SIZE: 10,
    FILE_SIZE_MB: 5,
  },
  PREMIUM: {
    REQUESTS_PER_MINUTE: 100,
    BATCH_SIZE: 100,
    FILE_SIZE_MB: 50,
  },
}