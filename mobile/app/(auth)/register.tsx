import React, { useState } from 'react'
import {
  View,
  Text,
  TextInput,
  TouchableOpacity,
  ActivityIndicator,
  KeyboardAvoidingView,
  Platform,
  Alert,
  ScrollView,
} from 'react-native'
import { useRouter } from 'expo-router'
import { useAuthStore } from '../../store/authStore'

export default function RegisterScreen() {
  const router = useRouter()
  const { register, isLoading } = useAuthStore()
  const [formData, setFormData] = useState({
    email: '',
    username: '',
    full_name: '',
    password: '',
    confirm_password: '',
  })

  const handleRegister = async () => {
    if (!formData.email || !formData.username || !formData.password) {
      Alert.alert('Error', 'Please fill in all required fields')
      return
    }

    if (formData.password !== formData.confirm_password) {
      Alert.alert('Error', 'Passwords do not match')
      return
    }

    if (formData.password.length < 8) {
      Alert.alert('Error', 'Password must be at least 8 characters')
      return
    }

    try {
      await register({
        email: formData.email,
        username: formData.username,
        full_name: formData.full_name,
        password: formData.password,
      })
      Alert.alert('Success', 'Account created! Please login.', [
        { text: 'OK', onPress: () => router.replace('/login') },
      ])
    } catch (error: any) {
      Alert.alert('Registration Failed', error.message || 'Something went wrong')
    }
  }

  return (
    <KeyboardAvoidingView
      behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
      className="flex-1 bg-gray-50 dark:bg-gray-950"
    >
      <ScrollView showsVerticalScrollIndicator={false}>
        <View className="flex-1 justify-center px-6 py-12">
          <View className="mb-8">
            <Text className="text-4xl font-bold text-center text-primary">
              SentinelMind
            </Text>
            <Text className="text-center text-gray-600 dark:text-gray-400 mt-2">
              Create your account
            </Text>
          </View>

          <View className="space-y-4">
            <View>
              <Text className="text-sm font-medium mb-2">Full Name (Optional)</Text>
              <TextInput
                className="bg-white dark:bg-gray-900 border border-gray-300 dark:border-gray-700 rounded-lg px-4 py-3"
                placeholder="John Doe"
                placeholderTextColor="#9ca3af"
                value={formData.full_name}
                onChangeText={(text) => setFormData({ ...formData, full_name: text })}
              />
            </View>

            <View>
              <Text className="text-sm font-medium mb-2">Username *</Text>
              <TextInput
                className="bg-white dark:bg-gray-900 border border-gray-300 dark:border-gray-700 rounded-lg px-4 py-3"
                placeholder="johndoe"
                placeholderTextColor="#9ca3af"
                value={formData.username}
                onChangeText={(text) => setFormData({ ...formData, username: text })}
                autoCapitalize="none"
              />
            </View>

            <View>
              <Text className="text-sm font-medium mb-2">Email *</Text>
              <TextInput
                className="bg-white dark:bg-gray-900 border border-gray-300 dark:border-gray-700 rounded-lg px-4 py-3"
                placeholder="you@example.com"
                placeholderTextColor="#9ca3af"
                value={formData.email}
                onChangeText={(text) => setFormData({ ...formData, email: text })}
                autoCapitalize="none"
                keyboardType="email-address"
              />
            </View>

            <View>
              <Text className="text-sm font-medium mb-2">Password *</Text>
              <TextInput
                className="bg-white dark:bg-gray-900 border border-gray-300 dark:border-gray-700 rounded-lg px-4 py-3"
                placeholder="Create a password"
                placeholderTextColor="#9ca3af"
                value={formData.password}
                onChangeText={(text) => setFormData({ ...formData, password: text })}
                secureTextEntry
              />
              <Text className="text-xs text-gray-500 mt-1">
                Min. 8 characters with uppercase, lowercase, and number
              </Text>
            </View>

            <View>
              <Text className="text-sm font-medium mb-2">Confirm Password *</Text>
              <TextInput
                className="bg-white dark:bg-gray-900 border border-gray-300 dark:border-gray-700 rounded-lg px-4 py-3"
                placeholder="Confirm your password"
                placeholderTextColor="#9ca3af"
                value={formData.confirm_password}
                onChangeText={(text) => setFormData({ ...formData, confirm_password: text })}
                secureTextEntry
              />
            </View>

            <TouchableOpacity
              onPress={handleRegister}
              disabled={isLoading}
              className="bg-primary py-3 rounded-lg mt-4"
            >
              {isLoading ? (
                <ActivityIndicator color="white" />
              ) : (
                <Text className="text-white text-center font-semibold">Create Account</Text>
              )}
            </TouchableOpacity>

            <TouchableOpacity onPress={() => router.push('/login')}>
              <Text className="text-center text-gray-600 dark:text-gray-400 mt-4">
                Already have an account?{' '}
                <Text className="text-primary font-semibold">Sign In</Text>
              </Text>
            </TouchableOpacity>
          </View>
        </View>
      </ScrollView>
    </KeyboardAvoidingView>
  )
}