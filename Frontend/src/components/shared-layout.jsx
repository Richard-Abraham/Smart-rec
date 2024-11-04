'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { Bell, ChevronDown, Menu, User } from 'lucide-react'
import { Button } from "../components/ui/button"
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "../components/ui/dropdown-menu"
import { Input } from "../components/ui/input"
import { useAuth } from '@/providers/AuthProvider'

export default function SharedLayout({ children }) {
  const [isSidebarOpen, setIsSidebarOpen] = useState(false)
  const router = useRouter()
  const { logout } = useAuth();

  return (
    <div className="flex h-screen bg-background overflow-hidden">
      {/* Sidebar */}
      <aside 
        className={`bg-card w-64 ${isSidebarOpen ? 'translate-x-0' : '-translate-x-full'} 
        transition-transform duration-300 ease-in-out fixed md:relative md:translate-x-0 h-full z-30
        border-r border-border/40 backdrop-blur supports-[backdrop-filter]:bg-background/60`}
      >
        <div className="flex items-center justify-between h-16 px-4 border-b border-border/40">
          <span 
            className="text-xl font-semibold bg-clip-text text-transparent bg-gradient-to-r from-primary to-blue-600 cursor-pointer"
            onClick={() => router.push('/')}
          >
            AttendanceOS
          </span>
          <Button 
            variant="ghost" 
            size="icon" 
            onClick={() => setIsSidebarOpen(false)}
            className="md:hidden"
          >
            <Menu className="h-6 w-6" />
          </Button>
        </div>
        <nav className="p-4">
          <ul className="space-y-2">
            <li>
              <Button 
                variant="ghost" 
                className="w-full justify-start"
                onClick={() => router.push('/?tab=facial-recognition')}
              >
                Dashboard
              </Button>
            </li>
            <li>
              <Button 
                variant="ghost" 
                className="w-full justify-start"
                onClick={() => router.push('/face-registration')}
              >
                Face Registration
              </Button>
            </li>
            <li>
              <Button 
                variant="ghost" 
                className="w-full justify-start"
                onClick={() => router.push('/players')}
              >
                Players
              </Button>
            </li>
            <li>
              <Button 
                variant="ghost" 
                className="w-full justify-start"
                onClick={() => router.push('/?tab=reports')}
              >
                Reports
              </Button>
            </li>
            <li>
              <Button 
                variant="ghost" 
                className="w-full justify-start"
                onClick={() => router.push('/settings')}
              >
                Settings
              </Button>
            </li>
          </ul>
        </nav>
      </aside>

      {/* Main content */}
      <div className="flex-1 flex flex-col min-h-screen overflow-hidden">
        <header className="bg-card border-b border-border/40 h-16 flex items-center justify-between px-4 sticky top-0 z-20 backdrop-blur supports-[backdrop-filter]:bg-background/60">
          <div className="flex items-center gap-4">
            {!isSidebarOpen && (
              <Button 
                variant="ghost" 
                size="icon" 
                onClick={() => setIsSidebarOpen(true)}
                className="md:hidden hover:bg-accent/50"
              >
                <Menu className="h-6 w-6" />
              </Button>
            )}
            <Input 
              type="search" 
              placeholder="Search..." 
              className="w-64 hidden md:block bg-background/60" 
            />
          </div>
          
          <div className="flex items-center gap-2">
            <Button variant="ghost" size="icon" className="hover:bg-accent/50">
              <Bell className="h-5 w-5" />
            </Button>
            
            <DropdownMenu>
              <DropdownMenuTrigger asChild>
                <Button variant="ghost" className="flex items-center gap-2 hover:bg-accent/50">
                  <User className="h-5 w-5" />
                  <span className="hidden md:inline">
                    {JSON.parse(localStorage.getItem('user'))?.email || 'User'}
                  </span>
                  <ChevronDown className="h-4 w-4" />
                </Button>
              </DropdownMenuTrigger>
              <DropdownMenuContent align="end" className="w-48">
                <DropdownMenuLabel>My Account</DropdownMenuLabel>
                <DropdownMenuSeparator />
                <DropdownMenuItem onClick={() => router.push('/settings')}>Settings</DropdownMenuItem>
                <DropdownMenuItem 
                  className="text-destructive"
                  onClick={() => {
                    logout();
                  }}
                >
                  Logout
                </DropdownMenuItem>
              </DropdownMenuContent>
            </DropdownMenu>
          </div>
        </header>

        <main className="flex-1 overflow-x-hidden overflow-y-auto bg-background/50 p-4 md:p-6">
          {children}
        </main>
      </div>
    </div>
  )
} 