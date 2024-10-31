import { useState, useRef } from 'react'
import Webcam from 'react-webcam'
import { supabase } from '@/lib/supabase'

export const FaceRegistration = () => {
    const webcamRef = useRef<Webcam>(null)
    const [registering, setRegistering] = useState(false)
    const [status, setStatus] = useState<'idle' | 'success' | 'error'>('idle')

    const handleRegistration = async () => {
        try {
            setRegistering(true)
            const imageSrc = webcamRef.current?.getScreenshot()
            if (!imageSrc) return

            const { data, error } = await supabase.functions.invoke('register-face', {
                body: { image: imageSrc }
            })

            setStatus(error ? 'error' : 'success')
        } catch (error) {
            setStatus('error')
        } finally {
            setRegistering(false)
        }
    }

    return (
        <div className="space-y-4">
            <Webcam
                ref={webcamRef}
                audio={false}
                screenshotFormat="image/jpeg"
                className="w-full max-w-md rounded-lg"
            />
            <button
                onClick={handleRegistration}
                disabled={registering}
                className="px-4 py-2 bg-blue-500 text-white rounded-lg"
            >
                {registering ? 'Registering...' : 'Register Face'}
            </button>
        </div>
    )
}