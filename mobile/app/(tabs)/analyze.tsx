import React, { useState } from 'react'
import {
  View,
  Text,
  TextInput,
  TouchableOpacity,
  ScrollView,
  ActivityIndicator,
  KeyboardAvoidingView,
  Platform
} from 'react-native'
import { useSentimentAnalysis } from '../../hooks/useSentimentAnalysis'
import { SentimentMeter } from '../../components/common/SentimentMeter'
import { EmotionWheel } from '../../components/analysis/EmotionWheel'
import { Mic, Camera, Send } from 'lucide-react-native'
import * as Haptics from 'expo-haptics'

export default function AnalyzeScreen() {
  const [text, setText] = useState('')
  const { analyze, results, isLoading, error } = useSentimentAnalysis()

  const handleAnalyze = async () => {
    if (!text.trim()) return
    
    Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Medium)
    await analyze(text)
  }

  const handleVoiceInput = () => {
    // Voice recording logic
    Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light)
  }

  const handleCameraOCR = () => {
    // Camera OCR logic
    Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light)
  }

  return (
    <KeyboardAvoidingView
      behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
      className="flex-1 bg-gray-50 dark:bg-gray-950"
    >
      <ScrollView className="flex-1" showsVerticalScrollIndicator={false}>
        <View className="p-6">
          {/* Header */}
          <Text className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
            Analyze Text
          </Text>
          <Text className="text-gray-600 dark:text-gray-400 mb-6">
            Enter text to analyze sentiment and emotions
          </Text>

          {/* Input Container */}
          <View className="bg-white dark:bg-gray-900 rounded-2xl shadow-lg p-4 mb-6">
            <TextInput
              className="text-gray-900 dark:text-white min-h-[120px] text-base"
              placeholder="Type or paste your text here..."
              placeholderTextColor="#9ca3af"
              multiline
              value={text}
              onChangeText={setText}
              editable={!isLoading}
            />

            <View className="flex-row justify-between items-center mt-4 pt-4 border-t border-gray-200 dark:border-gray-800">
              <TouchableOpacity
                onPress={handleVoiceInput}
                className="flex-row items-center"
                disabled={isLoading}
              >
                <Mic size={24} color="#3b82f6" />
                <Text className="ml-2 text-blue-500">Voice</Text>
              </TouchableOpacity>

              <TouchableOpacity
                onPress={handleCameraOCR}
                className="flex-row items-center"
                disabled={isLoading}
              >
                <Camera size={24} color="#3b82f6" />
                <Text className="ml-2 text-blue-500">OCR</Text>
              </TouchableOpacity>

              <TouchableOpacity
                onPress={handleAnalyze}
                disabled={isLoading || !text.trim()}
                className={`flex-row items-center px-4 py-2 rounded-full ${
                  isLoading || !text.trim()
                    ? 'bg-gray-300 dark:bg-gray-700'
                    : 'bg-blue-500'
                }`}
              >
                {isLoading ? (
                  <ActivityIndicator color="white" size="small" />
                ) : (
                  <>
                    <Send size={20} color="white" />
                    <Text className="ml-2 text-white font-semibold">Analyze</Text>
                  </>
                )}
              </TouchableOpacity>
            </View>
          </View>

          {/* Results */}
          {isLoading && (
            <View className="items-center py-8">
              <ActivityIndicator size="large" color="#3b82f6" />
              <Text className="text-gray-600 dark:text-gray-400 mt-4">
                Analyzing with AI...
              </Text>
            </View>
          )}

          {error && (
            <View className="bg-red-100 dark:bg-red-900/30 rounded-xl p-4">
              <Text className="text-red-600 dark:text-red-400 text-center">
                {error}
              </Text>
            </View>
          )}

          {results && (
            <View className="space-y-6">
              {/* Sentiment Meter */}
              <View className="bg-white dark:bg-gray-900 rounded-2xl p-6 shadow-lg">
                <Text className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
                  Sentiment Score
                </Text>
                <SentimentMeter
                  sentiment={results.sentiment}
                  confidence={results.confidence}
                />
                <View className="flex-row justify-between mt-6">
                  <View className="items-center">
                    <Text className="text-2xl font-bold text-red-500">
                      {results.probabilities.negative}%
                    </Text>
                    <Text className="text-sm text-gray-600 dark:text-gray-400">
                      Negative
                    </Text>
                  </View>
                  <View className="items-center">
                    <Text className="text-2xl font-bold text-gray-500">
                      {results.probabilities.neutral}%
                    </Text>
                    <Text className="text-sm text-gray-600 dark:text-gray-400">
                      Neutral
                    </Text>
                  </View>
                  <View className="items-center">
                    <Text className="text-2xl font-bold text-green-500">
                      {results.probabilities.positive}%
                    </Text>
                    <Text className="text-sm text-gray-600 dark:text-gray-400">
                      Positive
                    </Text>
                  </View>
                </View>
              </View>

              {/* Emotion Wheel */}
              {results.emotions && (
                <View className="bg-white dark:bg-gray-900 rounded-2xl p-6 shadow-lg">
                  <Text className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
                    Emotion Analysis
                  </Text>
                  <EmotionWheel emotions={results.emotions} />
                </View>
              )}

              {/* Insights */}
              <View className="bg-gradient-to-r from-blue-500 to-purple-600 rounded-2xl p-6">
                <Text className="text-white text-lg font-semibold mb-2">
                  AI Insights
                </Text>
                <Text className="text-white/90">
                  {results.sentiment === 'positive' &&
                    "Your text shows positive sentiment! Keep up the good energy."}
                  {results.sentiment === 'negative' &&
                    "The text shows negative sentiment. Consider reframing the message."}
                  {results.sentiment === 'neutral' &&
                    "Neutral sentiment detected. The text is factual and objective."}
                </Text>
              </View>
            </View>
          )}
        </View>
      </ScrollView>
    </KeyboardAvoidingView>
  )
}