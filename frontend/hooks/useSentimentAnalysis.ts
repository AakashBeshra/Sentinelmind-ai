import { useState, useCallback } from 'react'
import axios from 'axios'
import toast from 'react-hot-toast'

interface SentimentResult {
  sentiment: 'positive' | 'negative' | 'neutral'
  confidence: number
  probabilities: {
    positive: number
    negative: number
    neutral: number
  }
  emotions?: Record<string, number>
  dominant_emotion?: string
  processing_time_ms: number
}

export function useSentimentAnalysis() {
  const [isLoading, setIsLoading] = useState(false)
  const [results, setResults] = useState<SentimentResult | null>(null)
  const [error, setError] = useState<string | null>(null)

  const analyze = useCallback(async (text: string, options?: {
    includeEmotions?: boolean
    includeToxicity?: boolean
    language?: string
  }) => {
    if (!text.trim()) {
      toast.error('Please enter some text to analyze')
      return null
    }

    setIsLoading(true)
    setError(null)

    try {
      const response = await axios.post('/api/sentiment/analyze', {
        text: text.trim(),
        include_emotions: options?.includeEmotions ?? true,
        include_toxicity: options?.includeToxicity ?? false,
        language: options?.language ?? 'auto',
      }, {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('access_token')}`,
        },
      })

      const data = response.data
      setResults(data)
      toast.success('Analysis completed!')
      return data
    } catch (err: any) {
      const errorMessage = err.response?.data?.detail || 'Failed to analyze sentiment'
      setError(errorMessage)
      toast.error(errorMessage)
      return null
    } finally {
      setIsLoading(false)
    }
  }, [])

  const reset = useCallback(() => {
    setResults(null)
    setError(null)
  }, [])

  return {
    analyze,
    reset,
    isLoading,
    results,
    error,
  }
}