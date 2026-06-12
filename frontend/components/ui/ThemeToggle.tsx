'use client'

import React, { useEffect, useState } from 'react'
import { useTheme } from 'next-themes'
import { Sun, Moon, Monitor } from 'lucide-react'
import { motion } from 'framer-motion'

export const ThemeToggle: React.FC = () => {
  const [mounted, setMounted] = useState(false)
  const { theme, setTheme } = useTheme()

  useEffect(() => {
    setMounted(true)
  }, [])

  if (!mounted) {
    return <div className="w-9 h-9" />
  }

  return (
    <div className="flex items-center gap-1 bg-gray-100 dark:bg-gray-800 rounded-lg p-1">
      <motion.button
        whileTap={{ scale: 0.95 }}
        onClick={() => setTheme('light')}
        className={`p-2 rounded-md transition-colors ${
          theme === 'light'
            ? 'bg-white dark:bg-gray-700 shadow-sm'
            : 'text-gray-500 hover:text-gray-700 dark:text-gray-400'
        }`}
      >
        <Sun className="w-4 h-4" />
      </motion.button>
      <motion.button
        whileTap={{ scale: 0.95 }}
        onClick={() => setTheme('dark')}
        className={`p-2 rounded-md transition-colors ${
          theme === 'dark'
            ? 'bg-white dark:bg-gray-700 shadow-sm'
            : 'text-gray-500 hover:text-gray-700 dark:text-gray-400'
        }`}
      >
        <Moon className="w-4 h-4" />
      </motion.button>
      <motion.button
        whileTap={{ scale: 0.95 }}
        onClick={() => setTheme('system')}
        className={`p-2 rounded-md transition-colors ${
          theme === 'system'
            ? 'bg-white dark:bg-gray-700 shadow-sm'
            : 'text-gray-500 hover:text-gray-700 dark:text-gray-400'
        }`}
      >
        <Monitor className="w-4 h-4" />
      </motion.button>
    </div>
  )
}