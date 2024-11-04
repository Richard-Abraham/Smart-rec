'use client'

import { useState, useEffect } from 'react'
import { useSearchParams } from 'next/navigation'
import SharedLayout from '../components/shared-layout'
import { Tabs, TabsList, TabsTrigger, TabsContent } from "../components/ui/tabs"
import dynamic from 'next/dynamic'

// Dynamically import components with no SSR to avoid hydration issues
const FacialRecognition = dynamic(() => import('../components/facial-recognition.jsx'), { 
  ssr: false,
  loading: () => <div>Loading...</div>
})
const TimeTracking = dynamic(() => import('../components/time-tracking.jsx'), { 
  ssr: false,
  loading: () => <div>Loading...</div>
})
const RegistrationForm = dynamic(() => import('../components/registration-form.jsx'), { 
  ssr: false,
  loading: () => <div>Loading...</div>
})
const AttendanceTable = dynamic(() => import('../components/attendance-table.jsx'), { 
  ssr: false,
  loading: () => <div>Loading...</div>
})
const ReportsExport = dynamic(() => import('../components/reports-export.jsx'), { 
  ssr: false,
  loading: () => <div>Loading...</div>
})

export default function Dashboard() {
  const searchParams = useSearchParams()
  const [activeTab, setActiveTab] = useState('facial-recognition')

  useEffect(() => {
    const tab = searchParams.get('tab')
    if (tab) {
      setActiveTab(tab)
    }
  }, [searchParams])

  return (
    <SharedLayout>
      <div className="p-6">
        <h1 className="text-3xl font-bold mb-6">Dashboard</h1>
        <Tabs value={activeTab} onValueChange={setActiveTab} className="space-y-6">
          <TabsList className="bg-card">
            <TabsTrigger value="facial-recognition">Facial Recognition</TabsTrigger>
            <TabsTrigger value="time-tracking">Time Tracking</TabsTrigger>
            <TabsTrigger value="registration">Registration</TabsTrigger>
            <TabsTrigger value="attendance">Attendance</TabsTrigger>
            <TabsTrigger value="reports">Reports</TabsTrigger>
          </TabsList>

          <TabsContent value="facial-recognition" className="space-y-4">
            <div className="max-w-4xl mx-auto">
              <FacialRecognition />
            </div>
          </TabsContent>

          <TabsContent value="time-tracking" className="space-y-4">
            <div className="max-w-4xl mx-auto">
              <TimeTracking />
            </div>
          </TabsContent>

          <TabsContent value="registration" className="space-y-4">
            <div className="max-w-4xl mx-auto">
              <RegistrationForm />
            </div>
          </TabsContent>

          <TabsContent value="attendance" className="space-y-4">
            <div className="max-w-4xl mx-auto">
              <AttendanceTable />
            </div>
          </TabsContent>

          <TabsContent value="reports" className="space-y-4">
            <ReportsExport />
          </TabsContent>
        </Tabs>
      </div>
    </SharedLayout>
  )
}