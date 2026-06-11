import React, { useState } from 'react'
import {
  View,
  Text,
  TouchableOpacity,
  ActivityIndicator,
  Alert,
  ScrollView,
} from 'react-native'
import { Audio } from 'expo-av'
import { useRouter } from 'expo-router'
import { Mic, Square, Play, Trash2 } from 'lucide-react-native'
import { useAuthStore } from '../../store/authStore'

export default function VoiceRecorderScreen() {
  const router = useRouter()
  const { token } = useAuthStore()
  const [recording, setRecording] = useState<Audio.Recording | null>(null)
  const [isRecording, setIsRecording] = useState(false)
  const [processing, setProcessing] = useState(false)
  const [result, setResult] = useState<any>(null)
  const [sound, setSound] = useState<Audio.Sound | null>(null)

  const startRecording = async () => {
    try {
      await Audio.requestPermissionsAsync()
      await Audio.setAudioModeAsync({
        allowsRecordingIOS: true,
        playsInSilentModeIOS: true,
      })

      const { recording } = await Audio.Recording.createAsync(
        Audio.RecordingOptionsPresets.HIGH_QUALITY
      )
      setRecording(recording)
      setIsRecording(true)
    } catch (err) {
      Alert.alert('Error', 'Failed to start recording')
    }
  }

  const stopRecording = async () => {
    if (!recording) return

    setIsRecording(false)
    await recording.stopAndUnloadAsync()
    const uri = recording.getURI()
    setRecording(null)

    if (uri) {
      await analyzeAudio(uri)
    }
  }

  const analyzeAudio = async (uri: string) => {
    setProcessing(true)
    try {
      const formData = new FormData()
      formData.append('audio_file', {
        uri,
        type: 'audio/wav',
        name: 'recording.wav',
      } as any)

      const response = await fetch('http://localhost:8000/api/v1/voice/analyze', {
        method: 'POST',
        headers: {
          Authorization: `Bearer ${token}`,
          'Content-Type': 'multipart/form-data',
        },
        body: formData,
      })

      const data = await response.json()
      setResult(data)
    } catch (error) {
      Alert.alert('Error', 'Failed to analyze audio')
    } finally {
      setProcessing(false)
    }
  }

  const playRecording = async () => {
    if (result?.transcribed_text) {
      // In production, you would play the actual recording
      Alert.alert('Playback', 'Audio playback would start here')
    }
  }

  const reset = () => {
    setResult(null)
    if (sound) {
      sound.unloadAsync()
      setSound(null)
    }
  }

  return (
    <ScrollView className="flex-1 bg-gray-50 dark:bg-gray-950">
      <View className="p-6">
        <Text className="text-2xl font-bold text-gray-900 dark:text-white mb-2">
          Voice Analysis
        </Text>
        <Text className="text-gray-600 dark:text-gray-400 mb-6">
          Record your voice for sentiment analysis
        </Text>

        {!result && !processing && (
          <View className="items-center py-12">
            {isRecording ? (
              <TouchableOpacity
                onPress={stopRecording}
                className="bg-red-500 w-24 h-24 rounded-full items-center justify-center"
              >
                <Square size={32} color="white" />
              </TouchableOpacity>
            ) : (
              <TouchableOpacity
                onPress={startRecording}
                className="bg-primary w-24 h-24 rounded-full items-center justify-center"
              >
                <Mic size={32} color="white" />
              </TouchableOpacity>
            )}
            <Text className="mt-4 text-gray-600">
              {isRecording ? 'Recording... Tap to stop' : 'Tap to start recording'}
            </Text>
          </View>
        )}

        {processing && (
          <View className="items-center py-12">
            <ActivityIndicator size="large" color="#3b82f6" />
            <Text className="mt-4 text-gray-600">Analyzing your voice...</Text>
          </View>
        )}

        {result && (
          <View className="space-y-4">
            <View className="bg-white dark:bg-gray-900 rounded-2xl p-6">
              <Text className="text-lg font-semibold mb-2">Transcribed Text</Text>
              <Text className="text-gray-700 dark:text-gray-300">
                {result.transcribed_text || 'No text detected'}
              </Text>
            </View>

            <View className="bg-white dark:bg-gray-900 rounded-2xl p-6">
              <Text className="text-lg font-semibold mb-2">Sentiment Analysis</Text>
              <Text className="text-gray-700 dark:text-gray-300">
                Sentiment: {result.sentiment?.sentiment || 'N/A'}
              </Text>
              <Text className="text-gray-700 dark:text-gray-300 mt-1">
                Confidence: {((result.sentiment?.confidence || 0) * 100).toFixed(1)}%
              </Text>
            </View>

            {result.tone_analysis && (
              <View className="bg-white dark:bg-gray-900 rounded-2xl p-6">
                <Text className="text-lg font-semibold mb-2">Voice Tone Analysis</Text>
                <Text className="text-gray-700 dark:text-gray-300">
                  Tone: {result.tone_analysis.dominant_tone}
                </Text>
                <Text className="text-gray-700 dark:text-gray-300 mt-1">
                  {result.tone_analysis.tone_description}
                </Text>
              </View>
            )}

            <View className="flex-row gap-4 mt-4">
              <TouchableOpacity
                onPress={playRecording}
                className="flex-1 bg-primary py-3 rounded-lg flex-row items-center justify-center"
              >
                <Play size={20} color="white" />
                <Text className="text-white font-semibold ml-2">Play</Text>
              </TouchableOpacity>
              <TouchableOpacity
                onPress={reset}
                className="flex-1 bg-gray-500 py-3 rounded-lg flex-row items-center justify-center"
              >
                <Trash2 size={20} color="white" />
                <Text className="text-white font-semibold ml-2">New Recording</Text>
              </TouchableOpacity>
            </View>
          </View>
        )}
      </View>
    </ScrollView>
  )
}