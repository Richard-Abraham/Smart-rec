'use client'

import SharedLayout from '@/components/shared-layout'
import { Card, CardContent } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Search } from "lucide-react"

const players = [
  {
    id: 1,
    name: "John Smith",
    email: "john.smith@example.com",
    phone: "+1234567890",
    photo: "https://i.pravatar.cc/150?img=1",
    status: "Active",
    memberSince: "2024-01-15",
    lastAttendance: "2024-03-20"
  },
  {
    id: 2,
    name: "Sarah Johnson",
    email: "sarah.j@example.com",
    phone: "+1987654321",
    photo: "https://i.pravatar.cc/150?img=2",
    status: "Active",
    memberSince: "2024-02-01",
    lastAttendance: "2024-03-19"
  },
]

export default function PlayersPage() {
  return (
    <SharedLayout>
      <div className="p-6 space-y-6">
        <div className="flex justify-between items-center">
          <h1 className="text-3xl font-bold">Players</h1>
          <div className="flex gap-4">
            <Input
              placeholder="Search players..."
              className="w-64"
              type="search"
              icon={<Search className="h-4 w-4" />}
            />
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {players.map(player => (
            <Card key={player.id} className="hover:shadow-lg transition-shadow">
              <CardContent className="p-6">
                <div className="flex items-center space-x-4">
                  <img
                    src={player.photo}
                    alt={player.name}
                    className="w-16 h-16 rounded-full object-cover"
                  />
                  <div>
                    <h3 className="font-semibold text-lg">{player.name}</h3>
                    <p className="text-sm text-muted-foreground">{player.email}</p>
                    <div className="flex items-center gap-2 mt-2">
                      <span className={`px-2 py-1 rounded-full text-xs ${
                        player.status === 'Active' 
                          ? 'bg-green-100 text-green-700 dark:bg-green-900 dark:text-green-300'
                          : 'bg-yellow-100 text-yellow-700 dark:bg-yellow-900 dark:text-yellow-300'
                      }`}>
                        {player.status}
                      </span>
                      <span className="text-xs text-muted-foreground">
                        Member since {new Date(player.memberSince).toLocaleDateString()}
                      </span>
                    </div>
                  </div>
                </div>
                <div className="mt-4 text-sm text-muted-foreground">
                  Last attendance: {new Date(player.lastAttendance).toLocaleDateString()}
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    </SharedLayout>
  )
} 