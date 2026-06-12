'use client'

import React from 'react'
import {
  Radar,
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  ResponsiveContainer,
  Tooltip
} from 'recharts'
import { Card } from '@/components/common/Card'

interface EmotionRadarProps {
  emotions: Record<string, number>
}

export const EmotionRadar: React.FC<EmotionRadarProps> = ({ emotions }) => {
  const data = Object.entries(emotions).map(([emotion, value]) => ({
    emotion: emotion.charAt(0).toUpperCase() + emotion.slice(1),
    value: value * 100
  }))

  return (
    <Card className="p-6">
      <h3 className="text-lg font-semibold mb-4">Emotion Analysis</h3>
      <div style={{ height: 300 }}>
        <ResponsiveContainer width="100%" height="100%">
          <RadarChart data={data}>
            <PolarGrid />
            <PolarAngleAxis dataKey="emotion" />
            <PolarRadiusAxis domain={[0, 100]} />
            <Tooltip />
            <Radar
              name="Emotions"
              dataKey="value"
              stroke="#8884d8"
              fill="#8884d8"
              fillOpacity={0.6}
            />
          </RadarChart>
        </ResponsiveContainer>
      </div>
    </Card>
  )
}