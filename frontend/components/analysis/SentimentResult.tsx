'use client'

import React from 'react'
import { motion } from 'framer-motion'
import { Card } from '@/components/common/Card'
import { ConfidenceMeter } from './ConfidenceMeter'

interface SentimentResultProps {
  sentiment: string
  confidence: number
  probabilities: {
    positive: number
    negative: number
    neutral: number
  }
}

export const SentimentResult: React.FC<SentimentResultProps> = ({
  sentiment,
  confidence,
  probabilities
}) => {
  const getSentimentEmoji = () => {
    switch (sentiment) {
      case 'positive': return '😊'
      case 'negative': return '😞'
      default: return '😐'
    }
  }

  const getSentimentColor = () => {
    switch (sentiment) {
      case 'positive': return 'text-green-500'
      case 'negative': return 'text-red-500'
      default: return 'text-gray-500'
    }
  }

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ duration: 0.3 }}
    >
      <Card className="p-6">
        <div className="text-center mb-6">
          <div className="text-6xl mb-3">{getSentimentEmoji()}</div>
          <h3 className="text-2xl font-bold">
            Sentiment: <span className={getSentimentColor()}>
              {sentiment.charAt(0).toUpperCase() + sentiment.slice(1)}
            </span>
          </h3>
          <p className="text-gray-500 mt-1">Confidence: {(confidence * 100).toFixed(1)}%</p>
        </div>

        <div className="space-y-4">
          <ConfidenceMeter
            label="Positive"
            value={probabilities.positive * 100}
            color="#10b981"
          />
          <ConfidenceMeter
            label="Neutral"
            value={probabilities.neutral * 100}
            color="#6b7280"
          />
          <ConfidenceMeter
            label="Negative"
            value={probabilities.negative * 100}
            color="#ef4444"
          />
        </div>
      </Card>
    </motion.div>
  )
}