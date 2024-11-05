import { useEffect, useState } from 'react'
import { AttendanceService } from '@/services/attendance.service'

export const RealTimeAttendance = () => {
    const [records, setRecords] = useState([])
    const [loading, setLoading] = useState(true)
    const attendanceService = AttendanceService.getInstance()

    useEffect(() => {
        loadTodayAttendance()
        const unsubscribe = subscribeToUpdates()
        return () => unsubscribe()
    }, [])

    const loadTodayAttendance = async () => {
        try {
            const data = await attendanceService.getTodayAttendance()
            setRecords(data)
        } catch (error) {
            console.error('Failed to load attendance:', error)
        } finally {
            setLoading(false)
        }
    }

    const subscribeToUpdates = () => {
        return attendanceService.subscribeToAttendanceUpdates((newRecord) => {
            setRecords(prev => [newRecord, ...prev])
        })
    }

    return (
        <div className="space-y-4">
            <h2 className="text-2xl font-bold">Today's Attendance</h2>
            {loading ? (
                <div>Loading...</div>
            ) : (
                <AttendanceTable records={records} />
            )}
        </div>
    )
}