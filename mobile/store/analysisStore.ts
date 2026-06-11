import { create } from 'zustand'

interface Analysis {
  id: string
  text: string
  sentiment: string
  confidence: number
  emotions?: Record<string, number>
  created_at: string
}

interface AnalysisState {
  currentAnalysis: Analysis | null
  history: Analysis[]
  isLoading: boolean
  error: string | null
  setCurrentAnalysis: (analysis: Analysis | null) => void
  addToHistory: (analysis: Analysis) => void
  setLoading: (loading: boolean) => void
  setError: (error: string | null) => void
  clearHistory: () => void
}

export const useAnalysisStore = create<AnalysisState>((set) => ({
  currentAnalysis: null,
  history: [],
  isLoading: false,
  error: null,

  setCurrentAnalysis: (analysis) => set({ currentAnalysis: analysis }),

  addToHistory: (analysis) =>
    set((state) => ({
      history: [analysis, ...state.history].slice(0, 50),
    })),

  setLoading: (loading) => set({ isLoading: loading }),

  setError: (error) => set({ error }),

  clearHistory: () => set({ history: [] }),
}))