import { useState } from 'react'
import { Camera, CameraType } from 'expo-camera'

export const useCamera = () => {
  const [hasPermission, setHasPermission] = useState<boolean | null>(null)
  const [cameraRef, setCameraRef] = useState<Camera | null>(null)

  const requestPermission = async () => {
    const { status } = await Camera.requestCameraPermissionsAsync()
    setHasPermission(status === 'granted')
    return status === 'granted'
  }

  const takePicture = async () => {
    if (cameraRef) {
      const photo = await cameraRef.takePictureAsync({ base64: true })
      return photo
    }
    return null
  }

  return {
    hasPermission,
    cameraRef,
    setCameraRef,
    requestPermission,
    takePicture,
  }
}