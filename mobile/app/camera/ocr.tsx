import React, { useState, useRef } from 'react'
import {
  View,
  Text,
  TouchableOpacity,
  Image,
  ActivityIndicator,
  Alert,
  ScrollView,
} from 'react-native'
import { Camera, CameraType } from 'expo-camera'
import { useRouter } from 'expo-router'
import { useAuthStore } from '../../store/authStore'

export default function OCRScreen() {
  const router = useRouter()
  const { token } = useAuthStore()
  const [hasPermission, setHasPermission] = useState<boolean | null>(null)
  const [photo, setPhoto] = useState<string | null>(null)
  const [processing, setProcessing] = useState(false)
  const [result, setResult] = useState<any>(null)
  const cameraRef = useRef<Camera>(null)

  React.useEffect(() => {
    (async () => {
      const { status } = await Camera.requestCameraPermissionsAsync()
      setHasPermission(status === 'granted')
    })()
  }, [])

  const takePicture = async () => {
    if (cameraRef.current) {
      const photo = await cameraRef.current.takePictureAsync({ base64: true })
      setPhoto(photo.uri)
      processImage(photo.base64)
    }
  }

  const processImage = async (base64Image?: string) => {
    setProcessing(true)
    try {
      const formData = new FormData()
      if (photo) {
        formData.append('image', {
          uri: photo,
          type: 'image/jpeg',
          name: 'photo.jpg',
        } as any)
      }

      const response = await fetch('http://localhost:8000/api/v1/ocr/extract', {
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
      Alert.alert('Error', 'Failed to process image')
    } finally {
      setProcessing(false)
    }
  }

  const retake = () => {
    setPhoto(null)
    setResult(null)
  }

  if (hasPermission === null) {
    return (
      <View className="flex-1 justify-center items-center">
        <Text>Requesting camera permission...</Text>
      </View>
    )
  }

  if (hasPermission === false) {
    return (
      <View className="flex-1 justify-center items-center">
        <Text>No access to camera</Text>
        <TouchableOpacity onPress={() => router.back()} className="mt-4 bg-primary px-6 py-2 rounded-lg">
          <Text className="text-white">Go Back</Text>
        </TouchableOpacity>
      </View>
    )
  }

  if (photo) {
    return (
      <ScrollView className="flex-1 bg-gray-50 dark:bg-gray-950">
        <View className="p-6">
          <Image source={{ uri: photo }} className="w-full h-64 rounded-lg mb-4" />
          
          {processing ? (
            <View className="items-center py-8">
              <ActivityIndicator size="large" color="#3b82f6" />
              <Text className="mt-4 text-gray-600">Extracting text...</Text>
            </View>
          ) : result ? (
            <View className="bg-white dark:bg-gray-900 rounded-2xl p-6">
              <Text className="text-lg font-semibold mb-4">Extracted Text</Text>
              <Text className="text-gray-700 dark:text-gray-300 mb-4">
                {result.extracted_text || 'No text detected'}
              </Text>
              
              {result.sentiment_analysis && (
                <View className="mt-4 pt-4 border-t border-gray-200">
                  <Text className="text-lg font-semibold mb-2">Sentiment Analysis</Text>
                  <Text className="text-gray-700">
                    Sentiment: {result.sentiment_analysis.sentiment}
                  </Text>
                  <Text className="text-gray-700">
                    Confidence: {(result.sentiment_analysis.confidence * 100).toFixed(1)}%
                  </Text>
                </View>
              )}
            </View>
          ) : null}

          <View className="flex-row gap-4 mt-6">
            <TouchableOpacity
              onPress={retake}
              className="flex-1 bg-gray-500 py-3 rounded-lg"
            >
              <Text className="text-white text-center font-semibold">Retake</Text>
            </TouchableOpacity>
            <TouchableOpacity
              onPress={() => router.back()}
              className="flex-1 bg-primary py-3 rounded-lg"
            >
              <Text className="text-white text-center font-semibold">Done</Text>
            </TouchableOpacity>
          </View>
        </View>
      </ScrollView>
    )
  }

  return (
    <View className="flex-1">
      <Camera
        ref={cameraRef}
        style={{ flex: 1 }}
        type={CameraType.back}
      >
        <View className="flex-1 bg-transparent justify-end p-6">
          <TouchableOpacity
            onPress={takePicture}
            className="self-center bg-white w-20 h-20 rounded-full items-center justify-center mb-6"
          >
            <View className="w-16 h-16 bg-white rounded-full border-2 border-gray-300" />
          </TouchableOpacity>
          <TouchableOpacity
            onPress={() => router.back()}
            className="self-start absolute top-12 left-6 bg-black/50 p-3 rounded-full"
          >
            <Text className="text-white">Cancel</Text>
          </TouchableOpacity>
        </View>
      </Camera>
    </View>
  )
}