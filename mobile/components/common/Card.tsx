import React from 'react'
import { View, ViewProps } from 'react-native'

interface CardProps extends ViewProps {
  children: React.ReactNode
}

export const Card: React.FC<CardProps> = ({ children, className = '', ...props }) => {
  return (
    <View
      className={`bg-white dark:bg-gray-900 rounded-2xl shadow-sm ${className}`}
      {...props}
    >
      {children}
    </View>
  )
}