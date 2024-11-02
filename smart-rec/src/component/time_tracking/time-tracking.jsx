'use client'

import { useState, useEffect } from 'react'
import { Clock, Coffee } from 'lucide-react'
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"

export default function TimeTracking() {
  const [isCheckedIn, setIsCheckedIn] = useState(false)
  const [isOnBreak, setIsOnBreak] = useState(false)
  const [time, setTime] = useState(new Date())

  useEffect(() => {
    const timer = setInterval(() => setTime(new Date()), 1000)
    return () => clearInterval(timer)
  }, [])

  const handleCheckInOut = () => {
    setIsCheckedIn(!isCheckedIn)
    setIsOnBreak(false)
  }

  const handleBreak = () => {
    setIsOnBreak(!isOnBreak)
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>Time Tracking</CardTitle>
      </CardHeader>
      <CardContent className="flex flex-col items-center">
        <div className="text-4xl font-bold mb-4">
          {time.toLocaleTimeString()}
        </div>
        <div className="flex space-x-4 mb-4">
          <Button onClick={handleCheckInOut} variant={isCheckedIn ? "destructive" : "default"}>
            {isCheckedIn ? 'Check Out' : 'Check In'}
          </Button>
          <Button onClick={handleBreak} disabled={!isCheckedIn} variant={isOnBreak ? "secondary" : "outline"}>
            <Coffee className="mr-2 h-4 w-4" />
            {isOnBreak ? 'End Break' : 'Start Break'}
          </Button>
        </div>
        <div className="text-sm text-gray-500">
          {isCheckedIn ? (
            isOnBreak ? 'On Break' : 'Currently Working'
          ) : 'Not Checked In'}
        </div>
      </CardContent>
    </Card>
  )
}