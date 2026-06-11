import React from 'react'
import { View, Text } from 'react-native'

interface SentimentMeterProps {
  sentiment: 'positive' | 'negative' | 'neutral'
  confidence: number
  size?: 'small' | 'medium' | 'large'
}

export const SentimentMeter: React.FC<SentimentMeterProps> = ({
  sentiment,
  confidence,
  size = 'medium',
}) => {
  const getColor = () => {
    switch (sentiment) {
      case 'positive': return '#10b981'
      case 'negative': return '#ef4444'
      default: return '#6b7280'
    }
  }

  const getIcon = () => {
    switch (sentiment) {
      case 'positive': return '😊'
      case 'negative': return '😞'
      default: return '😐'
    }
  }

  const sizeClasses = {
    small: { text: 'text-sm', icon: 'text-lg', progress: 'h-1' },
    medium: { text: 'text-base', icon: 'text-2xl', progress: 'h-2' },
    large: { text: 'text-lg', icon: 'text-3xl', progress: 'h-3' },
  }

  const percentage = confidence * 100

  return (
    <View>
      <View className="flex-row items-center justify-between mb-2">
        <View className="flex-row items-center gap-2">
          <Text className={sizeClasses[size].icon}>{getIcon()}</Text>
          <Text className={`${sizeClasses[size].text} font-semibold`}>
            {sentiment.charAt(0).toUpperCase() + sentiment.slice(1)}
          </Text>
        </View>
        <Text className={`${sizeClasses[size].text} text-gray-600`}>
          {percentage.toFixed(0)}%
        </Text>
      </View>
      <View className={`bg-gray-200 rounded-full overflow-hidden ${sizeClasses[size].progress}`}>
        <View
          className={`bg-[${getColor()}] rounded-full`}
          style={{ width: `${percentage}%`, height: '100%' }}
        />
      </View>
    </View>
  )
}