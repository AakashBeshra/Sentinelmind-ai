import React from 'react'
import {
  View,
  Text,
  TouchableOpacity,
  Alert,
  ScrollView,
} from 'react-native'
import { useRouter } from 'expo-router'
import { useAuthStore } from '../../store/authStore'
import { User, Mail, LogOut, Crown, Settings } from 'lucide-react-native'

export default function ProfileScreen() {
  const router = useRouter()
  const { user, logout } = useAuthStore()

  const handleLogout = () => {
    Alert.alert('Logout', 'Are you sure you want to logout?', [
      { text: 'Cancel', style: 'cancel' },
      {
        text: 'Logout',
        style: 'destructive',
        onPress: () => {
          logout()
          router.replace('/login')
        },
      },
    ])
  }

  return (
    <ScrollView className="flex-1 bg-gray-50 dark:bg-gray-950">
      <View className="p-6">
        {/* Profile Header */}
        <View className="items-center mb-8">
          <View className="w-24 h-24 bg-primary rounded-full items-center justify-center mb-4">
            <Text className="text-3xl text-white font-bold">
              {user?.full_name?.charAt(0) || user?.username?.charAt(0) || 'U'}
            </Text>
          </View>
          <Text className="text-xl font-bold text-gray-900 dark:text-white">
            {user?.full_name || user?.username}
          </Text>
          <Text className="text-gray-600 dark:text-gray-400">
            @{user?.username}
          </Text>
        </View>

        {/* Account Info */}
        <View className="bg-white dark:bg-gray-900 rounded-2xl p-6 shadow-sm mb-6">
          <Text className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
            Account Information
          </Text>
          
          <View className="flex-row items-center mb-4">
            <User size={20} color="#6b7280" />
            <Text className="ml-3 text-gray-700 dark:text-gray-300">
              {user?.full_name || 'Not set'}
            </Text>
          </View>

          <View className="flex-row items-center">
            <Mail size={20} color="#6b7280" />
            <Text className="ml-3 text-gray-700 dark:text-gray-300">
              {user?.email}
            </Text>
          </View>
        </View>

        {/* Subscription */}
        <View className="bg-white dark:bg-gray-900 rounded-2xl p-6 shadow-sm mb-6">
          <View className="flex-row justify-between items-center mb-4">
            <Text className="text-lg font-semibold text-gray-900 dark:text-white">
              Subscription
            </Text>
            {user?.is_premium ? (
              <View className="flex-row items-center">
                <Crown size={16} color="#f59e0b" />
                <Text className="ml-1 text-amber-500 font-semibold">Premium</Text>
              </View>
            ) : (
              <TouchableOpacity
                onPress={() => router.push('/upgrade')}
                className="bg-primary px-4 py-2 rounded-lg"
              >
                <Text className="text-white font-semibold">Upgrade</Text>
              </TouchableOpacity>
            )}
          </View>
          
          {user?.is_premium ? (
            <Text className="text-gray-600 dark:text-gray-400">
              Enjoy unlimited access to all premium features
            </Text>
          ) : (
            <Text className="text-gray-600 dark:text-gray-400">
              Upgrade to premium for unlimited API calls and advanced features
            </Text>
          )}
        </View>

        {/* Actions */}
        <View className="bg-white dark:bg-gray-900 rounded-2xl p-6 shadow-sm">
          <TouchableOpacity
            onPress={() => router.push('/settings')}
            className="flex-row items-center py-3"
          >
            <Settings size={20} color="#6b7280" />
            <Text className="ml-3 text-gray-700 dark:text-gray-300 flex-1">
              Settings
            </Text>
          </TouchableOpacity>

          <TouchableOpacity
            onPress={handleLogout}
            className="flex-row items-center py-3 mt-2 border-t border-gray-200 dark:border-gray-800"
          >
            <LogOut size={20} color="#ef4444" />
            <Text className="ml-3 text-red-500 flex-1">Logout</Text>
          </TouchableOpacity>
        </View>
      </View>
    </ScrollView>
  )
}