from datetime import datetime
from typing import Dict, List, Optional
import uuid
from django.conf import settings
import asyncio
from collections import deque
from supabase import create_client
from models.attendance import Attendance

class AttendanceService:
    def __init__(self):
        self._updates_queue = deque(maxlen=100)
        self.supabase = create_client(
            settings.SUPABASE_URL,
            settings.SUPABASE_KEY
        )

    @classmethod
    async def get_today_records(cls) -> List[Dict]:
        today = datetime.now().date().isoformat()
        response = await cls.supabase.table('attendance')\
            .select("""
                *,
                profiles (
                    full_name,
                    department
                )
            """)\
            .gte('check_in', today)\
            .order('check_in', ascending=False)\
            .execute()
        
        return response.data if response.data else []

    @classmethod
    async def record_attendance(cls, user_id: str) -> Optional[Dict]:
        try:
            attendance = Attendance(
                id=str(uuid.uuid4()),
                user_id=user_id,
                timestamp=datetime.utcnow(),
                status=cls._get_status(),
                verification_method='face'
            )

            response = await cls.supabase.table('attendance').insert(attendance.dict()).execute()
            return response.data[0] if response.data else None

        except Exception as e:
            raise Exception(f"Error recording attendance: {str(e)}")

    def get_updates(self) -> Optional[Dict]:
        return self._updates_queue.popleft() if self._updates_queue else None

    @classmethod
    async def get_attendance_report(cls, date: str) -> List[Dict]:
        """Get attendance report for a specific date"""
        try:
            response = await cls.supabase.table('attendance')\
                .select("""
                    *,
                    users (
                        first_name,
                        last_name,
                    )
                """)\
                .eq('date', date)\
                .order('timestamp', ascending=True)\
                .execute()

            if not response.data:
                return []

            # Group by status
            report = {
                'total': len(response.data),
                'present': len([r for r in response.data if r['status'] == 'present']),
                'late': len([r for r in response.data if r['status'] == 'late']),
                'records': response.data
            }
            
            return report

        except Exception as e:
            raise Exception(f"Error generating attendance report: {str(e)}")