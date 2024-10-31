import face_recognition
import numpy as np
from django.conf import settings
from supabase import create_client
import cv2
from typing import Optional, Tuple

class FaceRecognitionService:
    def __init__(self):
        self.known_face_encodings = {}
        self.supabase = create_client(
            settings.SUPABASE_URL,
            settings.SUPABASE_KEY
        )
        self.load_face_encodings()
    
    @classmethod
    async def load_face_encodings(cls):
        """Load face encodings from Supabase"""
        response = await cls.supabase.table('face_encodings')\
            .select('user_id, encoding')\
            .eq('is_active', True)\
            .execute()
        
        if response.data:
            for record in response.data:
                cls.known_face_encodings[record['user_id']] = np.frombuffer(
                    record['encoding'], 
                    dtype=np.float64
                )

    @classmethod
    async def register_face(cls, user_id: str, image_array: np.ndarray) -> bool:
        face_encoding = cls.detect_and_encode_face(image_array)
        if not face_encoding:
            return False
            
        try:
            # Store in Supabase
            await cls.supabase.table('face_encodings').insert({
                'user_id': user_id,
                'encoding': face_encoding.tobytes(),
                'is_active': True
            }).execute()
            
            # Update local cache
            cls.known_face_encodings[user_id] = face_encoding
            return True
        except Exception as e:
            print(f"Error registering face: {str(e)}")
            return False