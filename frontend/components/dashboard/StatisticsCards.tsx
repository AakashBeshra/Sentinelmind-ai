'use client'

import React from 'react'
import { motion } from 'framer-motion'
import { Card } from '@/components/common/Card'
import { TrendingUp, TrendingDown, Minus, Activity } from 'lucide-react'

interface StatisticsCardsProps {
  stats: {
    total: number
    positive: number
    negative: number
    neutral: number
    averageConfidence: number
  }
}

export const StatisticsCards: React.FC<StatisticsCardsProps> = ({ stats }) => {
  const cards = [
    {
      title: 'Total Analyses',
      value: stats.total,
      icon: Activity,
      color: 'bg-blue-500',
      trend: '+12%'
    },
    {
      title: 'Positive',
      value: stats.positive,
      icon: TrendingUp,
      color: 'bg-green-500',
      trend: '+5%'
    },
    {
      title: 'Negative',
      value: stats.negative,
      icon: TrendingDown,
      color: 'bg-red-500',
      trend: '-3%'
    },
    {
      title: 'Neutral',
      value: stats.neutral,
      icon: Minus,
      color: 'bg-gray-500',
      trend: '0%'
    }
  ]

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      {cards.map((card, index) => (
        <motion.div
          key={card.title}
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: index * 0.1 }}
        >
          <Card className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-500 dark:text-gray-400">{card.title}</p>
                <p className="text-2xl font-bold mt-2">{card.value}</p>
                <p className="text-xs text-gray-500 mt-2">Trend: {card.trend}</p>
              </div>
              <div className={`p-3 rounded-full ${card.color} bg-opacity-10`}>
                <card.icon className={`w-6 h-6 ${card.color.replace('bg-', 'text-')}`} />
              </div>
            </div>
          </Card>
        </motion.div>
      ))}
    </div>
  )
}