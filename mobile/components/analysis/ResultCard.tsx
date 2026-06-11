import React from 'react'
import { View, Text } from 'react-native'

interface ResultCardProps {
  sentiment: string
  confidence: number
  emotions?: Record<string, number>
}

export const ResultCard: React.FC<ResultCardProps> = ({ sentiment, confidence, emotions }) => {
  const getSentimentColor = () => {
    switch (sentiment) {
      case 'positive': return '#10b981'
      case 'negative': return '#ef4444'
      default: return '#6b7280'
    }
  }

  const getSentimentEmoji = () => {
    switch (sentiment) {
      case 'positive': return '😊'
      case 'negative': return '😞'
      default: return '😐'
    }
  }

  const topEmotions = emotions
    ? Object.entries(emotions)
        .sort((a, b) => b[1] - a[1])
        .slice(0, 3)
    : []

  return (
    <View className="bg-white dark:bg-gray-900 rounded-2xl p-6 shadow-sm">
      <View className="items-center mb-4">
        <Text className="text-4xl mb-2">{getSentimentEmoji()}</Text>
        <Text className="text-xl font-bold" style={{ color: getSentimentColor() }}>
          {sentiment.charAt(0).toUpperCase() + sentiment.slice(1)}
        </Text>
        <Text className="text-gray-600 dark:text-gray-400 mt-1">
          Confidence: {(confidence * 100).toFixed(1)}%
        </Text>
      </View>

      {topEmotions.length > 0 && (
        <View className="mt-4 pt-4 border-t border-gray-200 dark:border-gray-800">
          <Text className="text-sm font-semibold mb-2">Top Emotions</Text>
          <View className="flex-row flex-wrap gap-2">
            {topEmotions.map(([emotion, score]) => (
              <View
                key={emotion}
                className="px-3 py-1 rounded-full bg-gray-100 dark:bg-gray-800"
              >
                <Text className="text-sm">
                  {emotion}: {(score * 100).toFixed(0)}%
                </Text>
              </View>
            ))}
          </View>
        </View>
      )}
    </View>
  )
}