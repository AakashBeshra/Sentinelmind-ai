'use client'

import React, { useState } from 'react'
import { Card } from '@/components/common/Card'
import { Button } from '@/components/common/Button'
import { Upload, Mic, FileText } from 'lucide-react'

interface TextInputProps {
  value: string
  onChange: (value: string) => void
  placeholder?: string
  className?: string
}

export const TextInput: React.FC<TextInputProps> = ({
  value,
  onChange,
  placeholder = "Enter your text here...",
  className = ""
}) => {
  const [charCount, setCharCount] = useState(0)

  const handleChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    const newValue = e.target.value
    setCharCount(newValue.length)
    onChange(newValue)
  }

  const handleFileUpload = () => {
    // Implement file upload
    console.log('File upload clicked')
  }

  const handleVoiceInput = () => {
    // Implement voice input
    console.log('Voice input clicked')
  }

  return (
    <Card className={`p-6 ${className}`}>
      <div className="space-y-4">
        <textarea
          value={value}
          onChange={handleChange}
          placeholder={placeholder}
          className="w-full h-64 p-4 border border-gray-300 dark:border-gray-700 rounded-lg 
                     focus:ring-2 focus:ring-primary focus:border-transparent
                     bg-white dark:bg-gray-900 text-gray-900 dark:text-white
                     resize-none"
        />
        
        <div className="flex justify-between items-center">
          <div className="flex gap-2">
            <Button variant="outline" size="sm" onClick={handleFileUpload}>
              <Upload className="w-4 h-4 mr-2" />
              Upload File
            </Button>
            <Button variant="outline" size="sm" onClick={handleVoiceInput}>
              <Mic className="w-4 h-4 mr-2" />
              Voice Input
            </Button>
          </div>
          
          <div className="text-sm text-gray-500">
            {charCount} / 5000 characters
          </div>
        </div>
      </div>
    </Card>
  )
}