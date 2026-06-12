'use client'

import React from 'react'
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts'
import { Card } from '@/components/common/Card'

interface TrendsGraphProps {
  data: Array<{
    date: string
    positive: number
    negative: number
    neutral: number
  }>
}

export const TrendsGraph: React.FC<TrendsGraphProps> = ({ data }) => {
  return (
    <Card className="p-6">
      <h3 className="text-lg font-semibold mb-4">Sentiment Trends Over Time</h3>
      <div style={{ height: 400 }}>
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={data}>
            <CartesianGrid strokeDasharray="3 3" className="stroke-gray-200 dark:stroke-gray-700" />
            <XAxis dataKey="date" className="text-xs" />
            <YAxis className="text-xs" />
            <Tooltip
              contentStyle={{
                backgroundColor: 'rgba(0,0,0,0.8)',
                borderRadius: '8px',
                border: 'none',
                color: '#fff',
              }}
            />
            <Legend />
            <Line
              type="monotone"
              dataKey="positive"
              stroke="#10b981"
              strokeWidth={2}
              dot={{ fill: '#10b981' }}
              name="Positive"
            />
            <Line
              type="monotone"
              dataKey="negative"
              stroke="#ef4444"
              strokeWidth={2}
              dot={{ fill: '#ef4444' }}
              name="Negative"
            />
            <Line
              type="monotone"
              dataKey="neutral"
              stroke="#6b7280"
              strokeWidth={2}
              dot={{ fill: '#6b7280' }}
              name="Neutral"
            />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </Card>
  )
}