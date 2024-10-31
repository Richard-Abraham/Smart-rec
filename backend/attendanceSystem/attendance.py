from datetime import datetime
from typing import Dict, List, Optional
from django.conf import settings
import asyncio
from collections import deque
from supabase import create_client
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
    async def record_attendance(cls, user_id: str, verification_method: str = 'face') -> Optional[Dict]:
        record = await super().record_attendance(user_id, verification_method)
        if record:
            cls._updates_queue.append(record)
        return record

    def get_updates(self) -> Optional[Dict]:
        return self._updates_queue.popleft() if self._updates_queue else None