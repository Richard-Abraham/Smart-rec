import { serve } from 'https://deno.land/std@0.168.0/http/server.ts'
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2'
import * as faceapi from 'https://esm.sh/@vladmandic/face-api'

serve(async (req) => {
  try {
    // Get image data from request
    const { image } = await req.json()
    
    // Initialize Supabase client
    const supabaseClient = createClient(
      Deno.env.get('SUPABASE_URL') ?? '',
      Deno.env.get('SUPABASE_ANON_KEY') ?? ''
    )

    // Convert base64 to buffer
    const imageBuffer = Buffer.from(image.split(',')[1], 'base64')

    // Load face-api models
    await faceapi.nets.ssdMobilenetv1.loadFromUri('/models')
    await faceapi.nets.faceLandmark68Net.loadFromUri('/models')
    await faceapi.nets.faceRecognitionNet.loadFromUri('/models')

    // Detect face and compute descriptors
    const img = await faceapi.bufferToImage(imageBuffer)
    const detection = await faceapi.detectSingleFace(img)
      .withFaceLandmarks()
      .withFaceDescriptor()

    if (!detection) {
      return new Response(
        JSON.stringify({ error: 'No face detected' }),
        { status: 400, headers: { 'Content-Type': 'application/json' } }
      )
    }

    // Store image in Supabase Storage
    const { data: storageData, error: storageError } = await supabaseClient
      .storage
      .from('face-images')
      .upload(`${Date.now()}.jpg`, imageBuffer, {
        contentType: 'image/jpeg'
      })

    if (storageError) {
      throw storageError
    }

    // Store face registration in database
    const { data, error } = await supabaseClient
      .from('face_registrations')
      .insert({
        image_url: storageData.path,
        face_encoding: detection.descriptor.toString(),
        user_id: req.headers.get('x-user-id')
      })
      .select()
      .single()

    if (error) {
      throw error
    }

    return new Response(
      JSON.stringify({ success: true, data }),
      { headers: { 'Content-Type': 'application/json' } }
    )
  } catch (error) {
    return new Response(
      JSON.stringify({ error: error.message }),
      { status: 500, headers: { 'Content-Type': 'application/json' } }
    )
  }
}) 