'use client'

import { useRef, useState } from 'react'
import Webcam from 'react-webcam'
import { Camera, Loader2 } from 'lucide-react'
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { supabase } from '@/lib/supabase'
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
                toast.error('Failed to capture image')
                return
            }

            // Get current user
            const { data: { user }, error: userError } = await supabase.auth.getUser()
            if (userError) throw userError

            // Upload photo to storage
            const fileName = `${user.id}/${Date.now()}.jpg`
            const { data: uploadData, error: uploadError } = await supabase.storage
                .from('face-photos')
                .upload(fileName, base64ToBlob(imageSrc), {
                    contentType: 'image/jpeg',
                    upsert: true
                })
            if (uploadError) throw uploadError

            // Get public URL for the uploaded photo
            const { data: { publicUrl } } = supabase.storage
                .from('face-photos')
                .getPublicUrl(fileName)

            // Create face encoding record
            const { data: faceData, error: faceError } = await supabase
                .from('face_encodings')
                .insert({
                    user_id: user.id,
                    photo_url: publicUrl,
                    is_active: true
                })
                .select()
                .single()

            if (faceError) throw faceError

            toast.success('Face registered successfully!')
        } catch (error) {
            console.error('Registration error:', error)
            toast.error(error.message || 'Failed to register face')
        } finally {
            setProcessing(false)
            setRegistering(false)
        }
    }

    // Helper function to convert base64 to blob
    const base64ToBlob = (base64) => {
        const byteString = atob(base64.split(',')[1])
        const mimeString = base64.split(',')[0].split(':')[1].split(';')[0]
        const ab = new ArrayBuffer(byteString.length)
        const ia = new Uint8Array(ab)
        
        for (let i = 0; i < byteString.length; i++) {
            ia[i] = byteString.charCodeAt(i)
        }
        
        return new Blob([ab], { type: mimeString })
    }

    return (
        <Card className="w-full max-w-4xl mx-auto backdrop-blur-sm bg-background/90">
            <CardHeader>
                <CardTitle className="text-2xl font-bold">Face Registration</CardTitle>
                <p className="text-sm text-muted-foreground">
                    Register your face for attendance tracking
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