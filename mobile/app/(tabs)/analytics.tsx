import React, { useEffect, useState } from 'react'
import {
  View,
  Text,
  ScrollView,
  ActivityIndicator,
  RefreshControl,
} from 'react-native'
import { useAuthStore } from '../../store/authStore'
import { StatsCard } from '../../components/dashboard/StatsCard'
import { SentimentMeter } from '../../components/common/SentimentMeter'

export default function AnalyticsScreen() {
  const { token } = useAuthStore()
  const [loading, setLoading] = useState(true)
  const [refreshing, setRefreshing] = useState(false)
  const [stats, setStats] = useState({
    total: 0,
    positive: 0,
    negative: 0,
    neutral: 0,
    averageConfidence: 0,
  })
  const [recentSentiment, setRecentSentiment] = useState<any[]>([])

  const fetchAnalytics = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/v1/analytics/dashboard?days=30', {
        headers: { Authorization: `Bearer ${token}` },
      })
      const data = await response.json()
      setStats({
        total: data.total_analyses || 0,
        positive: data.sentiment_distribution?.positive || 0,
        negative: data.sentiment_distribution?.negative || 0,
        neutral: data.sentiment_distribution?.neutral || 0,
        averageConfidence: data.average_confidence || 0,
      })
    } catch (error) {
      console.error('Failed to fetch analytics:', error)
    } finally {
      setLoading(false)
    }
  }

  const onRefresh = async () => {
    setRefreshing(true)
    await fetchAnalytics()
    setRefreshing(false)
  }

  useEffect(() => {
    fetchAnalytics()
  }, [])

  if (loading) {
    return (
      <View className="flex-1 justify-center items-center">
        <ActivityIndicator size="large" color="#3b82f6" />
      </View>
    )
  }

  const total = stats.total || 1
  const positivePercent = (stats.positive / total) * 100
  const negativePercent = (stats.negative / total) * 100
  const neutralPercent = (stats.neutral / total) * 100

  return (
    <ScrollView
      className="flex-1 bg-gray-50 dark:bg-gray-950"
      refreshControl={
        <RefreshControl refreshing={refreshing} onRefresh={onRefresh} />
      }
    >
      <View className="p-6">
        <Text className="text-2xl font-bold text-gray-900 dark:text-white mb-2">
          Analytics
        </Text>
        <Text className="text-gray-600 dark:text-gray-400 mb-6">
          Your sentiment analysis insights
        </Text>

        {/* Stats Grid */}
        <View className="flex-row flex-wrap justify-between mb-6">
          <StatsCard title="Total Analyses" value={stats.total} color="#3b82f6" />
          <StatsCard title="Positive" value={stats.positive} color="#10b981" />
          <StatsCard title="Negative" value={stats.negative} color="#ef4444" />
          <StatsCard title="Neutral" value={stats.neutral} color="#6b7280" />
        </View>

        {/* Sentiment Distribution */}
        <View className="bg-white dark:bg-gray-900 rounded-2xl p-6 shadow-sm mb-6">
          <Text className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
            Sentiment Distribution
          </Text>
          
          <View className="mb-4">
            <View className="flex-row justify-between mb-1">
              <Text className="text-sm text-gray-600">Positive</Text>
              <Text className="text-sm font-semibold text-green-500">
                {positivePercent.toFixed(1)}%
              </Text>
            </View>
            <View className="h-2 bg-gray-200 rounded-full overflow-hidden">
              <View
                className="h-full bg-green-500 rounded-full"
                style={{ width: `${positivePercent}%` }}
              />
            </View>
          </View>

          <View className="mb-4">
            <View className="flex-row justify-between mb-1">
              <Text className="text-sm text-gray-600">Negative</Text>
              <Text className="text-sm font-semibold text-red-500">
                {negativePercent.toFixed(1)}%
              </Text>
            </View>
            <View className="h-2 bg-gray-200 rounded-full overflow-hidden">
              <View
                className="h-full bg-red-500 rounded-full"
                style={{ width: `${negativePercent}%` }}
              />
            </View>
          </View>

          <View>
            <View className="flex-row justify-between mb-1">
              <Text className="text-sm text-gray-600">Neutral</Text>
              <Text className="text-sm font-semibold text-gray-500">
                {neutralPercent.toFixed(1)}%
              </Text>
            </View>
            <View className="h-2 bg-gray-200 rounded-full overflow-hidden">
              <View
                className="h-full bg-gray-500 rounded-full"
                style={{ width: `${neutralPercent}%` }}
              />
            </View>
          </View>
        </View>

        {/* Average Confidence */}
        <View className="bg-white dark:bg-gray-900 rounded-2xl p-6 shadow-sm">
          <Text className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
            Average Confidence
          </Text>
          <SentimentMeter
            sentiment={stats.averageConfidence > 0.7 ? 'positive' : 'neutral'}
            confidence={stats.averageConfidence}
            size="large"
          />
        </View>
      </View>
    </ScrollView>
  )
}