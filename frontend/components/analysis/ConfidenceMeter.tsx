'use client'

import React from 'react'
import { motion } from 'framer-motion'

interface ConfidenceMeterProps {
  label: string
  value: number
  color?: string
}

export const ConfidenceMeter: React.FC<ConfidenceMeterProps> = ({
  label,
  value,
  color = '#3b82f6',
}) => {
  const percentage = Math.min(100, Math.max(0, value))

  return (
    <div className="space-y-2">
      <div className="flex justify-between text-sm">
        <span className="font-medium">{label}</span>
        <span>{percentage.toFixed(1)}%</span>
      </div>
      <div className="h-2 bg-gray-200 dark:bg-gray-700 rounded-full overflow-hidden">
        <motion.div
          initial={{ width: 0 }}
          animate={{ width: `${percentage}%` }}
          transition={{ duration: 0.5, ease: 'easeOut' }}
          style={{ backgroundColor: color }}
          className="h-full rounded-full"
        />
      </div>
    </div>
  )
}