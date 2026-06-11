import React from 'react'
import { View, Text } from 'react-native'
import Svg, { Circle, Path, Text as SvgText } from 'react-native-svg'

interface EmotionWheelProps {
  emotions: Record<string, number>
  size?: number
}

const emotionColors: Record<string, string> = {
  joy: '#FFD700',
  sadness: '#4A90E2',
  anger: '#E74C3C',
  fear: '#8E44AD',
  love: '#FF69B4',
  surprise: '#F39C12',
}

export const EmotionWheel: React.FC<EmotionWheelProps> = ({ emotions, size = 250 }) => {
  const center = size / 2
  const radius = size * 0.35
  const emotionsList = Object.entries(emotions).filter(([_, value]) => value > 0.1)

  if (emotionsList.length === 0) {
    return (
      <View className="items-center justify-center" style={{ height: size }}>
        <Text className="text-gray-500">No emotions detected</Text>
      </View>
    )
  }

  const angleStep = (2 * Math.PI) / emotionsList.length

  return (
    <View className="items-center justify-center">
      <Svg width={size} height={size}>
        {emotionsList.map(([emotion, score], index) => {
          const startAngle = index * angleStep
          const endAngle = startAngle + angleStep
          
          const startX = center + radius * Math.cos(startAngle)
          const startY = center + radius * Math.sin(startAngle)
          const endX = center + radius * Math.cos(endAngle)
          const endY = center + radius * Math.sin(endAngle)
          
          const largeArcFlag = 0
          
          const pathData = `
            M ${center} ${center}
            L ${startX} ${startY}
            A ${radius} ${radius} 0 ${largeArcFlag} 1 ${endX} ${endY}
            Z
          `
          
          const labelAngle = startAngle + angleStep / 2
          const labelX = center + (radius + 20) * Math.cos(labelAngle)
          const labelY = center + (radius + 20) * Math.sin(labelAngle)
          
          return (
            <React.Fragment key={emotion}>
              <Path
                d={pathData}
                fill={emotionColors[emotion] || '#ccc'}
                opacity={Math.max(0.3, score)}
                stroke="#fff"
                strokeWidth="2"
              />
              <SvgText
                x={labelX}
                y={labelY}
                fontSize="12"
                fill="#333"
                textAnchor="middle"
                stroke="none"
              >
                {emotion.charAt(0).toUpperCase() + emotion.slice(1)}
              </SvgText>
            </React.Fragment>
          )
        })}
        <Circle cx={center} cy={center} r={radius * 0.3} fill="white" />
      </Svg>
    </View>
  )
}