import React, { useEffect, useState } from 'react'
import {
  View,
  Text,
  ScrollView,
  RefreshControl,
  TouchableOpacity,
  ActivityIndicator,
} from 'react-native'
import { useRouter } from 'expo-router'
import { useAuthStore } from '../../store/authStore'
import { StatsCard } from '../../components/dashboard/StatsCard'
import { SentimentMeter } from '../../components/common/SentimentMeter'
import { ResultCard } from '../../components/analysis/ResultCard'

export default function HomeScreen() {
  const router = useRouter()
  const { token, user } = useAuthStore()
  const [refreshing, setRefreshing] = useState(false)
  const [loading, setLoading] = useState(true)
  const [stats, setStats] = useState({
    total: 0,
    positive: 0,
    negative: 0,
    neutral: 0,
  })
  const [recentAnalysis, setRecentAnalysis] = useState<any>(null)

  const fetchDashboardData = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/v1/analytics/dashboard?days=7', {
        headers: { Authorization: `Bearer ${token}` },
      })
      const data = await response.json()
      
      setStats({
        total: data.total_analyses || 0,
        positive: data.sentiment_distribution?.positive || 0,
        negative: data.sentiment_distribution?.negative || 0,
        neutral: data.sentiment_distribution?.neutral || 0,
      })

      // Get most recent analysis
      if (data.recent_analyses && data.recent_analyses.length > 0) {
        setRecentAnalysis(data.recent_analyses[0])
      }
    } catch (error) {
      console.error('Failed to fetch dashboard data:', error)
    } finally {
      setLoading(false)
    }
  }

  const onRefresh = async () => {
    setRefreshing(true)
    await fetchDashboardData()
    setRefreshing(false)
  }

  useEffect(() => {
    fetchDashboardData()
  }, [])

  if (loading) {
    return (
      <View className="flex-1 justify-center items-center">
        <ActivityIndicator size="large" color="#3b82f6" />
      </View>
    )
  }

  return (
    <ScrollView
      className="flex-1 bg-gray-50 dark:bg-gray-950"
      refreshControl={
        <RefreshControl refreshing={refreshing} onRefresh={onRefresh} />
      }
    >
      <View className="p-6">
        {/* Welcome Header */}
        <View className="mb-6">
          <Text className="text-2xl font-bold text-gray-900 dark:text-white">
            Welcome back, {user?.full_name?.split(' ')[0] || user?.username}!
          </Text>
          <Text className="text-gray-600 dark:text-gray-400 mt-1">
            Here's your sentiment analysis summary
          </Text>
        </View>

        {/* Stats Grid */}
        <View className="flex-row flex-wrap justify-between mb-6">
          <StatsCard title="Total" value={stats.total} color="#3b82f6" />
          <StatsCard title="Positive" value={stats.positive} color="#10b981" />
          <StatsCard title="Negative" value={stats.negative} color="#ef4444" />
          <StatsCard title="Neutral" value={stats.neutral} color="#6b7280" />
        </View>

        {/* Quick Actions */}
        <View className="flex-row gap-4 mb-6">
          <TouchableOpacity
            onPress={() => router.push('/analyze')}
            className="flex-1 bg-primary py-4 rounded-2xl"
          >
            <Text className="text-white text-center font-semibold">New Analysis</Text>
          </TouchableOpacity>
          <TouchableOpacity
            onPress={() => router.push('/voice/recorder')}
            className="flex-1 bg-gray-200 dark:bg-gray-800 py-4 rounded-2xl"
          >
            <Text className="text-gray-900 dark:text-white text-center font-semibold">Voice Input</Text>
          </TouchableOpacity>
        </View>

        {/* Recent Analysis */}
        {recentAnalysis && (
          <View className="mb-6">
            <Text className="text-lg font-semibold text-gray-900 dark:text-white mb-3">
              Recent Analysis
            </Text>
            <ResultCard
              sentiment={recentAnalysis.sentiment}
              confidence={recentAnalysis.confidence}
              emotions={recentAnalysis.emotions}
            />
          </View>
        )}

        {/* Overall Sentiment */}
        <View className="bg-white dark:bg-gray-900 rounded-2xl p-6 shadow-sm">
          <Text className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
            Overall Sentiment
          </Text>
          <SentimentMeter
            sentiment={
              stats.positive > stats.negative && stats.positive > stats.neutral
                ? 'positive'
                : stats.negative > stats.positive && stats.negative > stats.neutral
                ? 'negative'
                : 'neutral'
            }
            confidence={
              Math.max(stats.positive, stats.negative, stats.neutral) / 
              (stats.positive + stats.negative + stats.neutral || 1)
            }
            size="large"
          />
        </View>
      </View>
    </ScrollView>
  )
}