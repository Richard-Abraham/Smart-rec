'use client'

import { useState } from 'react'
import { Bell, ChevronDown, Menu, User } from 'lucide-react'
import { Button } from "@/components/ui/button"
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"
import { Input } from "@/components/ui/input"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import FacialRecognition from './facial-recognition'
import TimeTracking from './time-tracking'
import RegistrationForm from './registration-form'
import AttendanceAnalytics from './attendance-analytics'
import ReportsExport from './reports-export'

export default function Dashboard() {
  const [isSidebarOpen, setIsSidebarOpen] = useState(true)

  return (
    <div className="flex h-screen bg-gray-100">
      {/* Sidebar */}
      <div className={`bg-white w-64 ${isSidebarOpen ? '' : 'hidden'} flex-shrink-0`}>
        <div className="flex items-center justify-between h-16 px-4 border-b">
          <span className="text-xl font-semibold">AttendanceOS</span>
          <Button variant="ghost" size="icon" onClick={() => setIsSidebarOpen(false)}>
            <Menu className="h-6 w-6" />
          </Button>
        </div>
        <nav className="p-4">
          <ul className="space-y-2">
            <li><Button variant="ghost" className="w-full justify-start">Dashboard</Button></li>
            <li><Button variant="ghost" className="w-full justify-start">Employees</Button></li>
            <li><Button variant="ghost" className="w-full justify-start">Reports</Button></li>
            <li><Button variant="ghost" className="w-full justify-start">Settings</Button></li>
          </ul>
        </nav>
      </div>

      {/* Main content */}
      <div className="flex-1 flex flex-col overflow-hidden">
        {/* Top bar */}
        <header className="bg-white border-b h-16 flex items-center justify-between px-4">
          {!isSidebarOpen && (
            <Button variant="ghost" size="icon" onClick={() => setIsSidebarOpen(true)}>
              <Menu className="h-6 w-6" />
            </Button>
          )}
          <div className="flex items-center">
            <Input type="search" placeholder="Search..." className="w-64 mr-4" />
            <Button variant="ghost" size="icon">
              <Bell className="h-5 w-5" />
            </Button>
          </div>
          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <Button variant="ghost" className="flex items-center">
                <User className="h-5 w-5 mr-2" />
                <span>John Doe</span>
                <ChevronDown className="h-4 w-4 ml-2" />
              </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent align="end">
              <DropdownMenuLabel>My Account</DropdownMenuLabel>
              <DropdownMenuSeparator />
              <DropdownMenuItem>Profile</DropdownMenuItem>
              <DropdownMenuItem>Settings</DropdownMenuItem>
              <DropdownMenuItem>Logout</DropdownMenuItem>
            </DropdownMenuContent>
          </DropdownMenu>
        </header>

        {/* Main content area */}
        <main className="flex-1 overflow-x-hidden overflow-y-auto bg-gray-100 p-6">
          <Tabs defaultValue="facial-recognition" className="space-y-4">
            <TabsList>
              <TabsTrigger value="facial-recognition">Facial Recognition</TabsTrigger>
              <TabsTrigger value="time-tracking">Time Tracking</TabsTrigger>
              <TabsTrigger value="registration">Registration</TabsTrigger>
              <TabsTrigger value="analytics">Analytics</TabsTrigger>
              <TabsTrigger value="reports">Reports</TabsTrigger>
            </TabsList>
            <TabsContent value="facial-recognition" className="p-4 bg-white rounded-lg shadow">
              <FacialRecognition />
            </TabsContent>
            <TabsContent value="time-tracking" className="p-4 bg-white rounded-lg shadow">
              <TimeTracking />
            </TabsContent>
            <TabsContent value="registration" className="p-4 bg-white rounded-lg shadow">
              <RegistrationForm />
            </TabsContent>
            <TabsContent value="analytics" className="p-4 bg-white rounded-lg shadow">
              <AttendanceAnalytics />
            </TabsContent>
            <TabsContent value="reports" className="p-4 bg-white rounded-lg shadow">
              <ReportsExport />
            </TabsContent>
          </Tabs>
        </main>
      </div>
    </div>
  )
}