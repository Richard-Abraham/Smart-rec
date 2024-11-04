'use client'

import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "../components/ui/table"
import { Card, CardContent, CardHeader, CardTitle } from "../components/ui/card"

export default function AttendanceTable() {
  // Sample data - replace with your actual data
  const attendanceData = [
    {
      id: 1,
      name: "John Doe",
      date: "2024-03-20",
      timeIn: "09:00 AM",
      timeOut: "05:00 PM",
      status: "Present",
    },
    // Add more sample data as needed
  ]

  return (
    <Card className="w-full">
      <CardHeader>
        <CardTitle>Attendance Records</CardTitle>
      </CardHeader>
      <CardContent>
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Name</TableHead>
              <TableHead>Date</TableHead>
              <TableHead>Time In</TableHead>
              <TableHead>Time Out</TableHead>
              <TableHead>Status</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {attendanceData.map((record) => (
              <TableRow key={record.id}>
                <TableCell>{record.name}</TableCell>
                <TableCell>{record.date}</TableCell>
                <TableCell>{record.timeIn}</TableCell>
                <TableCell>{record.timeOut}</TableCell>
                <TableCell>{record.status}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </CardContent>
    </Card>
  )
} 