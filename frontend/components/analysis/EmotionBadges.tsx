'use client'

import React from 'react'
import { motion } from 'framer-motion'

interface EmotionBadgesProps {
  emotions: Record<string, number>
}

const emotionColors: Record<string, string> = {
  joy: 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200',
  sadness: 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200',
  anger: 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200',
  fear: 'bg-purple-100 text-purple-800 dark:bg-purple-900 dark:text-purple-200',
  love: 'bg-pink-100 text-pink-800 dark:bg-pink-900 dark:text-pink-200',
  surprise: 'bg-orange-100 text-orange-800 dark:bg-orange-900 dark:text-orange-200'
}

export const EmotionBadges: React.FC<EmotionBadgesProps> = ({ emotions }) => {
  const sortedEmotions = Object.entries(emotions)
    .sort((a, b) => b[1] - a[1])
    .slice(0, 3)

  return (
    <div className="flex flex-wrap gap-2">
      {sortedEmotions.map(([emotion, score], index) => (
        <motion.div
          key={emotion}
          initial={{ opacity: 0, scale: 0.8 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: index * 0.1 }}
          className={`px-3 py-1 rounded-full text-sm font-medium ${emotionColors[emotion] || 'bg-gray-100'}`}
        >
          {emotion.charAt(0).toUpperCase() + emotion.slice(1)}: {(score * 100).toFixed(1)}%
        </motion.div>
      ))}
    </div>
  )
}