'use client'

import { useState, useRef } from 'react'
import Webcam from 'react-webcam'
import { Camera, Loader2 } from 'lucide-react'
import { Button } from "../components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "../components/ui/card"
import { supabase } from '../lib/supabase'
import { toast } from 'sonner'

export const FaceRegistration = () => {
    const webcamRef = useRef(null)
    const [registering, setRegistering] = useState(false)
    const [processing, setProcessing] = useState(false)

    const handleRegistration = async () => {
        if (!registering) {
            setRegistering(true)
            return
        }

        try {
            setProcessing(true)
            const imageSrc = webcamRef.current?.getScreenshot()
            if (!imageSrc) {
                throw new Error('Failed to capture image from webcam')
            }

            const blob = await fetch(imageSrc).then(r => r.blob())
            const fileName = `face_${Date.now()}.jpg`

            const { data: uploadData, error: uploadError } = await supabase.storage
                .from('face-photos')
                .upload(fileName, blob, {
                    contentType: 'image/jpeg',
                    cacheControl: '3600'
                })

            if (uploadError) throw uploadError

            const { data: { publicUrl } } = supabase.storage
                .from('face-photos')
                .getPublicUrl(fileName)

            const { data: { session }, error: sessionError } = await supabase.auth.getSession()
            if (sessionError) {
                throw new Error('Authentication required')
            }
            
            const userId = session?.user?.id
            if (!userId) {
                throw new Error('User not authenticated')
            }

            const { error: faceError } = await supabase
                .from('face_encodings')
                .insert({
                    user_id: userId,
                    photo_url: publicUrl,
                    is_active: true,
                    encoding: null
                })
                .select()
                .single()

            if (faceError) throw faceError

            toast.success('Face registered successfully!')
            setRegistering(false)
        } catch (error) {
            console.error('Registration error:', error)
            toast.error(error.message || 'Failed to register face')
            setRegistering(false)
        } finally {
            setProcessing(false)
        }
    }

    return (
        <Card className="w-full max-w-4xl mx-auto backdrop-blur-sm bg-background/90">
            <CardHeader>
                <CardTitle className="text-2xl font-bold">Face Registration</CardTitle>
                <p className="text-sm text-muted-foreground">
                    Position your face in the frame and click capture
                </p>
            </CardHeader>
            <CardContent className="flex flex-col items-center space-y-6">
                <div className="relative w-full max-w-md aspect-video bg-muted rounded-lg overflow-hidden border-2 border-primary/20">
                    {registering ? (
                        <Webcam
                            ref={webcamRef}
                            audio={false}
                            screenshotFormat="image/jpeg"
                            className="w-full h-full object-cover"
                            mirrored
                        />
                    ) : (
                        <div className="flex items-center justify-center h-full">
                            <Camera className="h-16 w-16 text-primary/40" />
                        </div>
                    )}
                    {processing && (
                        <div className="absolute inset-0 flex items-center justify-center bg-black/50">
                            <Loader2 className="h-8 w-8 animate-spin text-white" />
                        </div>
                    )}
                </div>
                <Button
                    onClick={handleRegistration}
                    disabled={processing}
                    className="w-48 h-12 text-lg font-semibold transition-all hover:scale-105"
                >
                    {processing ? 'Processing...' : registering ? 'Capture' : 'Start Camera'}
                </Button>
            </CardContent>
        </Card>
    )
}