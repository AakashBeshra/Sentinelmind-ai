import { io, Socket } from 'socket.io-client'

class WebSocketService {
  private socket: Socket | null = null
  
  connect(token: string) {
    this.socket = io(process.env.NEXT_PUBLIC_WS_URL || 'ws://localhost:8000', {
      path: '/ws/stream',
      query: { token },
      transports: ['websocket'],
    })
    
    this.socket.on('connect', () => {
      console.log('WebSocket connected')
    })
    
    this.socket.on('disconnect', () => {
      console.log('WebSocket disconnected')
    })
    
    return this.socket
  }
  
  disconnect() {
    if (this.socket) {
      this.socket.disconnect()
      this.socket = null
    }
  }
  
  sendMessage(message: any) {
    if (this.socket) {
      this.socket.emit('message', JSON.stringify(message))
    }
  }
  
  onAnalysis(callback: (data: any) => void) {
    if (this.socket) {
      this.socket.on('analysis', callback)
    }
  }
  
  onError(callback: (error: any) => void) {
    if (this.socket) {
      this.socket.on('error', callback)
    }
  }
}

export const websocketService = new WebSocketService()