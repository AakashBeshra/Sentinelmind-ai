import React from 'react'
import {
  TouchableOpacity,
  Text,
  ActivityIndicator,
  View,
  TouchableOpacityProps,
} from 'react-native'

interface ButtonProps extends TouchableOpacityProps {
  title: string
  variant?: 'primary' | 'secondary' | 'outline' | 'danger'
  size?: 'sm' | 'md' | 'lg'
  loading?: boolean
}

export const Button: React.FC<ButtonProps> = ({
  title,
  variant = 'primary',
  size = 'md',
  loading = false,
  className = '',
  disabled,
  ...props
}) => {
  const variantStyles = {
    primary: 'bg-primary',
    secondary: 'bg-gray-500',
    outline: 'bg-transparent border border-primary',
    danger: 'bg-red-500',
  }

  const sizeStyles = {
    sm: 'px-4 py-2',
    md: 'px-6 py-3',
    lg: 'px-8 py-4',
  }

  const textStyles = {
    primary: 'text-white',
    secondary: 'text-white',
    outline: 'text-primary',
    danger: 'text-white',
  }

  return (
    <TouchableOpacity
      className={`${variantStyles[variant]} ${sizeStyles[size]} rounded-lg ${className} ${
        disabled || loading ? 'opacity-50' : ''
      }`}
      disabled={disabled || loading}
      {...props}
    >
      {loading ? (
        <ActivityIndicator color={variant === 'outline' ? '#3b82f6' : 'white'} />
      ) : (
        <Text className={`${textStyles[variant]} text-center font-semibold`}>
          {title}
        </Text>
      )}
    </TouchableOpacity>
  )
}