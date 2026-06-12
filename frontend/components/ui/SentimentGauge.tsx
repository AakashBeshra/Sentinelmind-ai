'use client'

import React from 'react'

interface SentimentGaugeProps {
  score: number  // -100 to +100
  size?: 'sm' | 'md' | 'lg'
  showLabel?: boolean
  showValue?: boolean
}

export const SentimentGauge: React.FC<SentimentGaugeProps> = ({
  score,
  size = 'md',
  showLabel = true,
  showValue = true
}) => {
  // Clamp score between -100 and 100
  const clampedScore = Math.max(-100, Math.min(100, score))
  const percentage = (clampedScore + 100) / 2 // Convert -100..100 to 0..100
  
  // Determine color based on score
  const getColor = () => {
    if (clampedScore >= 50) return '#10b981' // Green - very positive
    if (clampedScore >= 20) return '#84cc16' // Lime - positive
    if (clampedScore > -20) return '#6b7280' // Gray - neutral
    if (clampedScore > -50) return '#f97316' // Orange - negative
    return '#ef4444' // Red - very negative
  }
  
  // Get sentiment label
  const getLabel = () => {
    if (clampedScore >= 60) return 'Very Positive'
    if (clampedScore >= 20) return 'Positive'
    if (clampedScore > -20) return 'Neutral'
    if (clampedScore > -60) return 'Negative'
    return 'Very Negative'
  }
  
  // Get emoji
  const getEmoji = () => {
    if (clampedScore >= 60) return '😍'
    if (clampedScore >= 20) return '🙂'
    if (clampedScore > -20) return '😐'
    if (clampedScore > -60) return '😞'
    return '😫'
  }
  
  // Size configurations
  const sizes = {
    sm: {
      container: 'w-32 h-32',
      text: 'text-sm',
      valueText: 'text-lg',
      strokeWidth: 8,
      fontSize: '0.875rem'
    },
    md: {
      container: 'w-48 h-48',
      text: 'text-base',
      valueText: 'text-2xl',
      strokeWidth: 10,
      fontSize: '1rem'
    },
    lg: {
      container: 'w-64 h-64',
      text: 'text-lg',
      valueText: 'text-3xl',
      strokeWidth: 12,
      fontSize: '1.25rem'
    }
  }
  
  const config = sizes[size]
  const radius = 40
  const circumference = 2 * Math.PI * radius
  const offset = circumference - (percentage / 100) * circumference
  const color = getColor()
  
  return (
    <div className={`flex flex-col items-center ${config.container}`}>
      {/* Gauge */}
      <div className="relative">
        <svg
          width="100%"
          height="100%"
          viewBox="0 0 120 120"
          className="transform -rotate-90"
        >
          {/* Background circle */}
          <circle
            cx="60"
            cy="60"
            r={radius}
            fill="none"
            stroke="#e5e7eb"
            strokeWidth={config.strokeWidth}
            className="dark:stroke-gray-700"
          />
          
          {/* Progress circle */}
          <circle
            cx="60"
            cy="60"
            r={radius}
            fill="none"
            stroke={color}
            strokeWidth={config.strokeWidth}
            strokeDasharray={circumference}
            strokeDashoffset={offset}
            strokeLinecap="round"
            className="transition-all duration-700 ease-out"
          />
        </svg>
        
        {/* Center content */}
        <div className="absolute inset-0 flex flex-col items-center justify-center">
          <span className={`${config.valueText} font-bold`} style={{ color }}>
            {clampedScore > 0 ? '+' : ''}{Math.round(clampedScore)}%
          </span>
          {showValue && (
            <span className={`${config.text} text-gray-500 dark:text-gray-400`}>
              Score
            </span>
          )}
        </div>
      </div>
      
      {/* Label and Emoji */}
      {showLabel && (
        <div className="mt-3 text-center">
          <span className="text-3xl mb-1 block">{getEmoji()}</span>
          <p className={`font-medium ${config.text}`} style={{ color }}>
            {getLabel()}
          </p>
        </div>
      )}
    </div>
  )
}

export default SentimentGauge