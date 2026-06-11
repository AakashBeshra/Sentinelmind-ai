import { Stack } from 'expo-router'
import { StatusBar } from 'expo-status-bar'

export default function RootLayout() {
  return (
    <>
      <StatusBar style="auto" />
      <Stack
        screenOptions={{
          headerShown: false,
          contentStyle: { backgroundColor: '#f9fafb' },
        }}
      >
        <Stack.Screen name="(auth)" options={{ headerShown: false }} />
        <Stack.Screen name="(tabs)" options={{ headerShown: false }} />
        <Stack.Screen name="camera/ocr" options={{ headerShown: true, title: 'OCR Scanner' }} />
        <Stack.Screen name="voice/recorder" options={{ headerShown: true, title: 'Voice Recorder' }} />
      </Stack>
    </>
  )
}