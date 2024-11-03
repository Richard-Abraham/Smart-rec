'use client'

import { useState } from "react"
import { format } from "date-fns"
import { Calendar as CalendarIcon, Search, Mail, Phone } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Calendar } from "@/components/ui/calendar"
import { Input } from "@/components/ui/input"
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@/components/ui/popover"
import { cn } from "@/lib/utils"

// Sample player data
const players = [
  {
    id: 1,
    name: "John Smith",
    email: "john.smith@example.com",
    phone: "+1234567890",
    attendance: 15,
    lastPayment: "2024-02-15",
    amountPaid: 150,
    balance: 50,
  },
  {
    id: 2,
    name: "Sarah Johnson",
    email: "sarah.j@example.com",
    phone: "+1987654321",
    attendance: 12,
    lastPayment: "2024-03-01",
    amountPaid: 200,
    balance: 100,
  },
]

export default function ReportsExport() {
  const [date, setDate] = useState()
  const [searchQuery, setSearchQuery] = useState("")
  const [searchResults, setSearchResults] = useState([])

  const handleSearch = (query) => {
    const results = players.filter(player => 
      player.name.toLowerCase().includes(query.toLowerCase())
    )
    setSearchResults(query ? results : [])
  }

  const handleNotify = async (player, type) => {
    // Simulate sending notification
    console.log(`Sending ${type} notification to ${player.name}`)
    
    if (type === 'email') {
      // Simulate email API call
      await new Promise(resolve => setTimeout(resolve, 1000))
      alert(`Email sent to ${player.email}`)
    } else {
      // Simulate SMS API call
      await new Promise(resolve => setTimeout(resolve, 1000))
      alert(`SMS sent to ${player.phone}`)
    }
  }

  const handleExport = async () => {
    if (!date) return
    
    try {
      // Simulate export process
      console.log(`Exporting report for ${format(date, "yyyy-MM-dd")}`)
      await new Promise(resolve => setTimeout(resolve, 1000))
      
      // Create sample export data
      const exportData = {
        date: format(date, "yyyy-MM-dd"),
        players: players.map(player => ({
          name: player.name,
          attendance: player.attendance,
          balance: player.balance
        }))
      }
      
      // Simulate file download
      const blob = new Blob([JSON.stringify(exportData, null, 2)], { type: 'application/json' })
      const url = window.URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = `attendance-report-${format(date, "yyyy-MM-dd")}.json`
      document.body.appendChild(a)
      a.click()
      window.URL.revokeObjectURL(url)
      document.body.removeChild(a)
      
      alert('Report exported successfully!')
    } catch (error) {
      console.error('Export failed:', error)
      alert('Failed to export report. Please try again.')
    }
  }

  return (
    <div className="space-y-6">
      <Card className="w-full max-w-lg mx-auto">
        <CardHeader>
          <CardTitle>Export Reports</CardTitle>
          <CardDescription>
            Select a date to export attendance reports
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="grid gap-4">
            <Popover>
              <PopoverTrigger asChild>
                <Button
                  variant="outline"
                  className={cn(
                    "w-full justify-start text-left font-normal",
                    !date && "text-muted-foreground"
                  )}
                >
                  <CalendarIcon className="mr-2 h-4 w-4" />
                  {date ? format(date, "PPP") : "Pick a date"}
                </Button>
              </PopoverTrigger>
              <PopoverContent className="w-auto p-0" align="start">
                <Calendar
                  mode="single"
                  selected={date}
                  onSelect={setDate}
                  initialFocus
                />
              </PopoverContent>
            </Popover>
          </div>
          <Button 
            className="w-full" 
            onClick={handleExport}
            disabled={!date}
          >
            Export Report
          </Button>
        </CardContent>
      </Card>

      <Card className="w-full">
        <CardHeader>
          <CardTitle>Player Payment Reports</CardTitle>
          <CardDescription>
            Search players to view attendance and payment details
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-6">
          <div className="flex gap-4">
            <Input
              placeholder="Search player name..."
              value={searchQuery}
              onChange={(e) => {
                setSearchQuery(e.target.value)
                handleSearch(e.target.value)
              }}
              className="max-w-sm"
            />
            <Button variant="secondary" onClick={() => handleSearch(searchQuery)}>
              <Search className="h-4 w-4 mr-2" />
              Search
            </Button>
          </div>

          {searchResults.length > 0 && (
            <div className="border rounded-lg divide-y">
              {searchResults.map(player => (
                <div key={player.id} className="p-4 space-y-4">
                  <div className="flex justify-between items-start">
                    <div>
                      <h3 className="font-semibold">{player.name}</h3>
                      <p className="text-sm text-muted-foreground">
                        Attendance: {player.attendance} sessions
                      </p>
                      <p className="text-sm text-muted-foreground">
                        Last Payment: {player.lastPayment} (${player.amountPaid})
                      </p>
                      <p className="text-sm font-medium text-destructive">
                        Outstanding Balance: ${player.balance}
                      </p>
                    </div>
                    <div className="flex gap-2">
                      <Button 
                        variant="outline" 
                        size="sm"
                        onClick={() => handleNotify(player, 'email')}
                      >
                        <Mail className="h-4 w-4 mr-2" />
                        Email
                      </Button>
                      <Button 
                        variant="outline" 
                        size="sm"
                        onClick={() => handleNotify(player, 'sms')}
                      >
                        <Phone className="h-4 w-4 mr-2" />
                        SMS
                      </Button>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}

          {searchQuery && searchResults.length === 0 && (
            <p className="text-center text-muted-foreground">No players found</p>
          )}
        </CardContent>
      </Card>
    </div>
  )
} 