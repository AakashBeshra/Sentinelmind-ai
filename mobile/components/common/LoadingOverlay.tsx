import React from 'react'
import { View, ActivityIndicator, Text, Modal } from 'react-native'

interface LoadingOverlayProps {
  visible: boolean
  message?: string
}

export const LoadingOverlay: React.FC<LoadingOverlayProps> = ({ visible, message }) => {
  if (!visible) return null

  return (
    <Modal transparent visible={visible} animationType="fade">
      <View className="flex-1 bg-black/50 justify-center items-center">
        <View className="bg-white dark:bg-gray-900 rounded-2xl p-6 items-center">
          <ActivityIndicator size="large" color="#3b82f6" />
          {message && (
            <Text className="mt-4 text-gray-700 dark:text-gray-300">{message}</Text>
          )}
        </View>
      </View>
    </Modal>
  )
}