import * as SecureStore from 'expo-secure-store'

export const secureStorage = {
  async setItem(key: string, value: string): Promise<void> {
    await SecureStore.setItemAsync(key, value)
  },

  async getItem(key: string): Promise<string | null> {
    return await SecureStore.getItemAsync(key)
  },

  async removeItem(key: string): Promise<void> {
    await SecureStore.deleteItemAsync(key)
  },

  async setToken(token: string): Promise<void> {
    await this.setItem('access_token', token)
  },

  async getToken(): Promise<string | null> {
    return await this.getItem('access_token')
  },

  async removeToken(): Promise<void> {
    await this.removeItem('access_token')
  },
}