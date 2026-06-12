import { createSlice, PayloadAction } from '@reduxjs/toolkit'

interface Analysis {
  id: string
  text: string
  sentiment: string
  confidence: number
  timestamp: string
}

interface AnalysisState {
  currentAnalysis: any | null
  history: Analysis[]
  isLoading: boolean
  error: string | null
}

const initialState: AnalysisState = {
  currentAnalysis: null,
  history: [],
  isLoading: false,
  error: null,
}

const analysisSlice = createSlice({
  name: 'analysis',
  initialState,
  reducers: {
    setCurrentAnalysis: (state, action: PayloadAction<any>) => {
      state.currentAnalysis = action.payload
    },
    addToHistory: (state, action: PayloadAction<Analysis>) => {
      state.history.unshift(action.payload)
      if (state.history.length > 50) {
        state.history.pop()
      }
    },
    setLoading: (state, action: PayloadAction<boolean>) => {
      state.isLoading = action.payload
    },
    setError: (state, action: PayloadAction<string | null>) => {
      state.error = action.payload
    },
    clearHistory: (state) => {
      state.history = []
    },
  },
})

export const { setCurrentAnalysis, addToHistory, setLoading, setError, clearHistory } = analysisSlice.actions
export default analysisSlice.reducer