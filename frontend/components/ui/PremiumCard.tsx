'use client'

import React from 'react'
import { motion } from 'framer-motion'
import { Card } from '@/components/common/Card'
import { Button } from '@/components/common/Button'
import { Crown, Zap, Globe, BarChart, Users, Shield } from 'lucide-react'

interface PremiumCardProps {
  variant?: 'monthly' | 'yearly'
  onUpgrade?: () => void
}

const features = [
  { icon: Zap, text: 'Unlimited API calls' },
  { icon: Globe, text: 'Batch processing (up to 1000 texts)' },
  { icon: BarChart, text: 'Advanced analytics & insights' },
  { icon: Users, text: 'Team collaboration' },
  { icon: Shield, text: 'Priority support' },
]

export const PremiumCard: React.FC<PremiumCardProps> = ({
  variant = 'monthly',
  onUpgrade,
}) => {
  const price = variant === 'monthly' ? '$49' : '$499'
  const period = variant === 'monthly' ? '/month' : '/year'
  const savings = variant === 'yearly' ? 'Save 15%' : null

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ duration: 0.3 }}
    >
      <Card className="relative overflow-hidden p-8 border-2 border-primary">
        {/* Badge */}
        <div className="absolute top-4 right-4">
          <div className="flex items-center gap-1 bg-primary/10 text-primary px-3 py-1 rounded-full text-sm">
            <Crown className="w-3 h-3" />
            <span>Premium</span>
          </div>
        </div>

        {/* Price */}
        <div className="text-center mb-6">
          <div className="text-4xl font-bold">
            {price}
            <span className="text-lg font-normal text-gray-500">{period}</span>
          </div>
          {savings && (
            <div className="text-sm text-green-500 mt-1">{savings}</div>
          )}
        </div>

        {/* Features */}
        <div className="space-y-3 mb-8">
          {features.map((feature, index) => (
            <div key={index} className="flex items-center gap-3">
              <feature.icon className="w-4 h-4 text-primary" />
              <span className="text-sm">{feature.text}</span>
            </div>
          ))}
        </div>

        {/* Button */}
        <Button
          onClick={onUpgrade}
          className="w-full"
          size="lg"
        >
          Upgrade to Premium
        </Button>

        <p className="text-xs text-gray-500 text-center mt-4">
          Cancel anytime. No questions asked.
        </p>
      </Card>
    </motion.div>
  )
}