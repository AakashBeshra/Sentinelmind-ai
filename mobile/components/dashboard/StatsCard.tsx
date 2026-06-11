import React from 'react'
import { View, Text } from 'react-native'

interface StatsCardProps {
  title: string
  value: number
  color: string
}

export const StatsCard: React.FC<StatsCardProps> = ({ title, value, color }) => {
  return (
    <View className="w-[48%] bg-white dark:bg-gray-900 rounded-xl p-4 shadow-sm mb-4">
      <Text className="text-sm text-gray-600 dark:text-gray-400 mb-2">{title}</Text>
      <Text className="text-2xl font-bold" style={{ color }}>
        {value}
      </Text>
    </View>
  )
}