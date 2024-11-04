'use client'

import SharedLayout from '../../components/shared-layout'
import { FaceRegistration } from '../../components/FaceRegistration'

export default function FaceRegistrationPage() {
  return (
    <SharedLayout>
      <div className="p-6">
        <h1 className="text-3xl font-bold mb-6">Face Registration</h1>
        <FaceRegistration />
      </div>
    </SharedLayout>
  )
} 