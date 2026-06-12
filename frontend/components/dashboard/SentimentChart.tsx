'use client'

import React from 'react'
import {
  LineChart,
  Line,
  AreaChart,
  Area,
  BarChart,
  Bar,
  PieChart,
  Pie,
  Cell,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer
} from 'recharts'
import { motion } from 'framer-motion'
import { Card } from '@/components/common/Card'

interface SentimentChartProps {
  data: Array<{
    date: string
    positive: number
    negative: number
    neutral: number
  }>
  type?: 'line' | 'area' | 'bar' | 'pie'
  height?: number
}

const COLORS = ['#10b981', '#ef4444', '#6b7280']

export const SentimentChart: React.FC<SentimentChartProps> = ({
  data,
  type = 'area',
  height = 400
}) => {
  const renderChart = () => {
    switch (type) {
      case 'line':
        return (
          <LineChart data={data}>
            <CartesianGrid strokeDasharray="3 3" className="stroke-muted" />
            <XAxis dataKey="date" className="text-xs" />
            <YAxis className="text-xs" />
            <Tooltip
              contentStyle={{
                backgroundColor: 'rgba(0,0,0,0.8)',
                borderRadius: '8px',
                border: 'none',
                color: '#fff'
              }}
            />
            <Legend />
            <Line
              type="monotone"
              dataKey="positive"
              stroke="#10b981"
              strokeWidth={2}
              dot={{ fill: '#10b981' }}
            />
            <Line
              type="monotone"
              dataKey="negative"
              stroke="#ef4444"
              strokeWidth={2}
              dot={{ fill: '#ef4444' }}
            />
            <Line
              type="monotone"
              dataKey="neutral"
              stroke="#6b7280"
              strokeWidth={2}
              dot={{ fill: '#6b7280' }}
            />
          </LineChart>
        )
      
      case 'area':
        return (
          <AreaChart data={data}>
            <CartesianGrid strokeDasharray="3 3" className="stroke-muted" />
            <XAxis dataKey="date" />
            <YAxis />
            <Tooltip
              contentStyle={{
                backgroundColor: 'rgba(0,0,0,0.8)',
                borderRadius: '8px',
                border: 'none'
              }}
            />
            <Legend />
            <Area
              type="monotone"
              dataKey="positive"
              stackId="1"
              stroke="#10b981"
              fill="#10b981"
              fillOpacity={0.3}
            />
            <Area
              type="monotone"
              dataKey="negative"
              stackId="1"
              stroke="#ef4444"
              fill="#ef4444"
              fillOpacity={0.3}
            />
            <Area
              type="monotone"
              dataKey="neutral"
              stackId="1"
              stroke="#6b7280"
              fill="#6b7280"
              fillOpacity={0.3}
            />
          </AreaChart>
        )
      
      case 'bar':
        return (
          <BarChart data={data}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="date" />
            <YAxis />
            <Tooltip />
            <Legend />
            <Bar dataKey="positive" fill="#10b981" />
            <Bar dataKey="negative" fill="#ef4444" />
            <Bar dataKey="neutral" fill="#6b7280" />
          </BarChart>
        )
      
      case 'pie':
        const lastData = data[data.length - 1]
        const pieData = [
          { name: 'Positive', value: lastData?.positive || 0 },
          { name: 'Negative', value: lastData?.negative || 0 },
          { name: 'Neutral', value: lastData?.neutral || 0 }
        ]
        return (
          <PieChart>
            <Pie
              data={pieData}
              cx="50%"
              cy="50%"
              labelLine={false}
              label={(entry) => `${entry.name}: ${entry.value}%`}
              outerRadius={80}
              fill="#8884d8"
              dataKey="value"
            >
              {pieData.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
              ))}
            </Pie>
            <Tooltip />
            <Legend />
          </PieChart>
        )
    }
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
    >
      <Card className="p-6">
        <h3 className="text-lg font-semibold mb-4">Sentiment Trends</h3>
        <div style={{ height }}>
          <ResponsiveContainer width="100%" height="100%">
            {renderChart()}
          </ResponsiveContainer>
        </div>
      </Card>
    </motion.div>
  )
}