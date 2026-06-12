import { createSlice, PayloadAction } from '@reduxjs/toolkit'

interface UIState {
  theme: 'light' | 'dark' | 'system'
  sidebarOpen: boolean
  notifications: Array<{
    id: string
    message: string
    type: 'info' | 'success' | 'error' | 'warning'
    read: boolean
  }>
}

const initialState: UIState = {
  theme: 'system',
  sidebarOpen: true,
  notifications: [],
}

const uiSlice = createSlice({
  name: 'ui',
  initialState,
  reducers: {
    setTheme: (state, action: PayloadAction<'light' | 'dark' | 'system'>) => {
      state.theme = action.payload
      if (typeof window !== 'undefined') {
        localStorage.setItem('theme', action.payload)
      }
    },
    toggleSidebar: (state) => {
      state.sidebarOpen = !state.sidebarOpen
    },
    addNotification: (state, action: PayloadAction<Omit<UIState['notifications'][0], 'id' | 'read'>>) => {
      state.notifications.push({
        id: Date.now().toString(),
        ...action.payload,
        read: false,
      })
    },
    markNotificationRead: (state, action: PayloadAction<string>) => {
      const notification = state.notifications.find(n => n.id === action.payload)
      if (notification) {
        notification.read = true
      }
    },
    clearNotifications: (state) => {
      state.notifications = []
    },
  },
})

export const { setTheme, toggleSidebar, addNotification, markNotificationRead, clearNotifications } = uiSlice.actions
export default uiSlice.reducer