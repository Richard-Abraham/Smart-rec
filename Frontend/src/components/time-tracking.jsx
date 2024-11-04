'use client'

import { useState, useEffect } from 'react'
import { Clock, Coffee } from 'lucide-react'
import { Button } from "../components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "../components/ui/card"

export default function TimeTracking() {
  const [isCheckedIn, setIsCheckedIn] = useState(false)
  const [isOnBreak, setIsOnBreak] = useState(false)
  const [currentTime, setCurrentTime] = useState(null)
  const [checkInTime, setCheckInTime] = useState(null)
  const [totalTime, setTotalTime] = useState('00:00:00')

  useEffect(() => {
    // Initialize currentTime after component mounts
    setCurrentTime(new Date())
    
    const timer = setInterval(() => {
      setCurrentTime(new Date())
      if (isCheckedIn && !isOnBreak && checkInTime) {
        const diff = new Date().getTime() - checkInTime.getTime()
        const hours = Math.floor(diff / 3600000).toString().padStart(2, '0')
        const minutes = Math.floor((diff % 3600000) / 60000).toString().padStart(2, '0')
        const seconds = Math.floor((diff % 60000) / 1000).toString().padStart(2, '0')
        setTotalTime(`${hours}:${minutes}:${seconds}`)
      }
    }, 1000)

    return () => clearInterval(timer)
  }, [isCheckedIn, isOnBreak, checkInTime])

  const handleCheckInOut = () => {
    if (!isCheckedIn) {
      setCheckInTime(new Date())
    } else {
      setCheckInTime(null)
      setTotalTime('00:00:00')
    }
    setIsCheckedIn(!isCheckedIn)
    setIsOnBreak(false)
  }

  if (!currentTime) {
    return null // or a loading spinner
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>Time Tracking</CardTitle>
      </CardHeader>
      <CardContent className="flex flex-col items-center space-y-6">
        <div className="text-4xl font-mono">
          {currentTime.toLocaleTimeString('en-US', { hour12: false })}
        </div>
        
        <div className="text-2xl font-mono text-gray-600">
          Total Time: {totalTime}
        </div>

        <div className="flex space-x-4">
          <Button 
            onClick={handleCheckInOut}
            variant={isCheckedIn ? "destructive" : "default"}
            className="w-32"
          >
            <Clock className="mr-2 h-4 w-4" />
            {isCheckedIn ? 'Check Out' : 'Check In'}
          </Button>

          <Button
            onClick={() => setIsOnBreak(!isOnBreak)}
            disabled={!isCheckedIn}
            variant={isOnBreak ? "secondary" : "outline"}
            className="w-32"
          >
            <Coffee className="mr-2 h-4 w-4" />
            {isOnBreak ? 'End Break' : 'Take Break'}
          </Button>
        </div>

        <div className="text-sm text-gray-500">
          {isCheckedIn ? (
            isOnBreak ? 'Currently on break' : (
              checkInTime && `Checked in at ${checkInTime.toLocaleTimeString('en-US', { hour12: false })}`
            )
          ) : 'Not checked in'}
        </div>
      </CardContent>
    </Card>
  )
} 