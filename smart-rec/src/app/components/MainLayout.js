'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { Menu } from 'lucide-react'

export default function MainLayout({ children }) {
  const [isSidebarOpen, setIsSidebarOpen] = useState(false)
  const router = useRouter()

  return (
    <div className="flex h-screen bg-background overflow-hidden">
      {/* Sidebar */}
      <aside className={`bg-card w-64 ${isSidebarOpen ? 'translate-x-0' : '-translate-x-full'} 
        transition-transform duration-300 ease-in-out fixed md:relative md:translate-x-0 h-full z-30
        border-r border-border/40 backdrop-blur`}>
        <nav className="p-4">
          <ul className="space-y-2">
            <li>
              <button 
                className="w-full text-left px-4 py-2 rounded hover:bg-accent"
                onClick={() => router.push('/?tab=facial-recognition')}
              >
                Dashboard
              </button>
            </li>
            <li>
              <button 
                className="w-full text-left px-4 py-2 rounded hover:bg-accent"
                onClick={() => router.push('/face-registration')}
              >
                Face Registration
              </button>
            </li>
            <li>
              <button 
                className="w-full text-left px-4 py-2 rounded hover:bg-accent"
                onClick={() => router.push('/settings')}
              >
                Settings
              </button>
            </li>
          </ul>
        </nav>
      </aside>

      {/* Main content */}
      <div className="flex-1 flex flex-col min-h-screen overflow-hidden">
        <header className="bg-card border-b h-16 flex items-center px-4">
          <button
            className="md:hidden"
            onClick={() => setIsSidebarOpen(!isSidebarOpen)}
          >
            <Menu className="h-6 w-6" />
          </button>
        </header>
        <main className="flex-1 overflow-x-hidden overflow-y-auto bg-background/50 p-4 md:p-6">
          {children}
        </main>
      </div>
    </div>
  )
} 