'use client'

import React, { useEffect, useRef } from 'react'
import { Card } from '@/components/common/Card'

interface WordCloudProps {
  words: Array<{ word: string; count: number }>
  maxWords?: number
}

export const WordCloud: React.FC<WordCloudProps> = ({ words, maxWords = 50 }) => {
  const canvasRef = useRef<HTMLCanvasElement>(null)

  useEffect(() => {
    if (!canvasRef.current || !words.length) return

    const canvas = canvasRef.current
    const ctx = canvas.getContext('2d')
    if (!ctx) return

    // Set canvas size
    canvas.width = canvas.offsetWidth
    canvas.height = 300

    // Clear canvas
    ctx.clearRect(0, 0, canvas.width, canvas.height)

    // Sort words by count and take top N
    const topWords = [...words]
      .sort((a, b) => b.count - a.count)
      .slice(0, maxWords)

    // Calculate font sizes (min 12px, max 48px)
    const maxCount = topWords[0]?.count || 1
    const minCount = topWords[topWords.length - 1]?.count || 1

    // Simple word placement (random positions for demo)
    topWords.forEach((word, index) => {
      const fontSize = 12 + (word.count / maxCount) * 36
      ctx.font = `${fontSize}px Arial`
      
      const x = 20 + (index % 10) * (canvas.width / 10)
      const y = 30 + Math.floor(index / 10) * 40
      
      // Random color based on word
      const hue = (word.word.length * 50) % 360
      ctx.fillStyle = `hsl(${hue}, 70%, 50%)`
      
      ctx.fillText(word.word, x, y)
    })
  }, [words])

  if (!words.length) {
    return (
      <Card className="p-6">
        <h3 className="text-lg font-semibold mb-4">Keyword Cloud</h3>
        <div className="h-[300px] flex items-center justify-center text-gray-500">
          No keywords available
        </div>
      </Card>
    )
  }

  return (
    <Card className="p-6">
      <h3 className="text-lg font-semibold mb-4">Keyword Cloud</h3>
      <canvas
        ref={canvasRef}
        className="w-full h-[300px]"
        style={{ width: '100%', height: '300px' }}
      />
    </Card>
  )
}