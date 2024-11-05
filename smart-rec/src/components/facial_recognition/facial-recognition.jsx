'use client'

import { useState, useRef, useEffect } from 'react'
import { Camera } from 'lucide-react'
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"

export default function FacialRecognition() {
  const [isDetecting, setIsDetecting] = useState(false)
  const videoRef = useRef(null)

  useEffect(() => {
    if (isDetecting && videoRef.current) {
      navigator.mediaDevices.getUserMedia({ video: true })
        .then(stream => {
          if (videoRef.current) {
            videoRef.current.srcObject = stream
          }
        })
        .catch(err => console.error("Error accessing camera:", err))
    } else if (!isDetecting && videoRef.current && videoRef.current.srcObject) {
      const stream = videoRef.current.srcObject;
      const tracks = stream.getTracks()
      tracks.forEach(track => track.stop())
    }
  }, [isDetecting])

  const toggleDetection = () => {
    setIsDetecting(!isDetecting)
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>Real-time Facial Detection</CardTitle>
      </CardHeader>
      <CardContent className="flex flex-col items-center">
        <div className="relative w-full max-w-md aspect-video bg-gray-200 rounded-lg overflow-hidden mb-4">
          {isDetecting ? (
            <video ref={videoRef} autoPlay className="w-full h-full object-cover" />
          ) : (
            <div className="flex items-center justify-center h-full">
              <Camera className="h-16 w-16 text-gray-400" />
            </div>
          )}
        </div>
        <Button onClick={toggleDetection}>
          {isDetecting ? 'Stop Detection' : 'Start Detection'}
        </Button>
      </CardContent>
    </Card>
  )
}
