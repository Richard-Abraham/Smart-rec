'use client'

import { useState, useRef } from 'react'
import { Camera } from 'lucide-react'
import { Button } from "../components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "../components/ui/card"
import Webcam from 'react-webcam'

export default function FacialRecognition() {
  const [isCapturing, setIsCapturing] = useState(false)
  const webcamRef = useRef(null)

  const handleCapture = async () => {
    if (!isCapturing) {
      setIsCapturing(true)
      return
    }

    const imageSrc = webcamRef.current?.getScreenshot()
    if (imageSrc) {
      console.log('Captured image:', imageSrc)
      // Here you would typically send the image to your backend
    }
    setIsCapturing(false)
  }

  return (
    <Card className="w-full max-w-4xl mx-auto bg-card/50 backdrop-blur-sm border border-border/50">
      <CardHeader>
        <CardTitle className="text-2xl font-bold text-primary">Facial Recognition</CardTitle>
      </CardHeader>
      <CardContent className="flex flex-col items-center space-y-6">
        <div className="relative w-full max-w-md aspect-video bg-muted/20 rounded-lg overflow-hidden border border-border/50">
          {isCapturing ? (
            <Webcam
              ref={webcamRef}
              audio={false}
              screenshotFormat="image/jpeg"
              className="w-full h-full object-cover"
            />
          ) : (
            <div className="flex items-center justify-center h-full">
              <Camera className="h-16 w-16 text-muted-foreground" />
            </div>
          )}
        </div>
        <Button 
          onClick={handleCapture}
          className="w-48 h-12 text-lg font-medium hover:scale-105 transition-transform"
        >
          {isCapturing ? 'Capture' : 'Start Camera'}
        </Button>
      </CardContent>
    </Card>
  )
} 