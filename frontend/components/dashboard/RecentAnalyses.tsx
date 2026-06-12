'use client'

import React from 'react'
import { Card } from '@/components/common/Card'
import { formatDistanceToNow } from 'date-fns'

interface Analysis {
  id: string
  text: string
  sentiment: string
  timestamp: string
}

interface RecentAnalysesProps {
  analyses: Analysis[]
}

export const RecentAnalyses: React.FC<RecentAnalysesProps> = ({ analyses }) => {
  const getSentimentColor = (sentiment: string) => {
    switch (sentiment) {
      case 'positive': return 'text-green-500'
      case 'negative': return 'text-red-500'
      default: return 'text-gray-500'
    }
  }

  return (
    <Card className="p-6">
      <h3 className="text-lg font-semibold mb-4">Recent Analyses</h3>
      <div className="space-y-4">
        {analyses.map((analysis) => (
          <div key={analysis.id} className="border-b border-gray-200 dark:border-gray-700 pb-3 last:border-0">
            <p className="text-gray-700 dark:text-gray-300 line-clamp-2">
              {analysis.text}
            </p>
            <div className="flex justify-between items-center mt-2">
              <span className={`font-medium ${getSentimentColor(analysis.sentiment)}`}>
                {analysis.sentiment.charAt(0).toUpperCase() + analysis.sentiment.slice(1)}
              </span>
              <span className="text-sm text-gray-500">
                {formatDistanceToNow(new Date(analysis.timestamp), { addSuffix: true })}
              </span>
            </div>
          </div>
        ))}
      </div>
    </Card>
  )
}