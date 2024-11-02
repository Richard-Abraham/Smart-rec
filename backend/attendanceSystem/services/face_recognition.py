import face_recognition
import numpy as np
from django.conf import settings
from supabase import create_client
import cv2
from typing import Optional, Dict
import base64
from models.face_encoding import FaceEncoding
from uuid import UUID

class FaceRecognitionService:
    def __init__(self):
        self.known_face_encodings: Dict[UUID, np.ndarray] = {}
        self.supabase = create_client(
            settings.SUPABASE_URL,
            settings.SUPABASE_KEY
        )
        self.load_face_encodings()
    
    @classmethod
    async def load_face_encodings(cls):
        """Load face encodings from Supabase"""
        response = await cls.supabase.table('face_encodings')\
            .select('*')\
            .eq('is_active', True)\
            .execute()
        
        if response.data:
            for record in response.data:
                encoding = FaceEncoding(**record)
                cls.known_face_encodings[encoding.user_id] = encoding.to_numpy()

    @classmethod
    async def register_face(cls, body: dict) -> Dict:
        try:
            user_id = UUID(body['user_id'])
            image_data = body['image']  # Base64 encoded image
            
            # Upload image to storage bucket
            photo_url = await cls.storage.upload_photo(str(user_id), image_data)
            if not photo_url:
                raise Exception("Failed to upload photo")

            # Process image for face encoding
            image_array = np.frombuffer(base64.b64decode(image_data.split(',')[1]), np.uint8)
            image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
            rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            
            # Get face encoding
            face_locations = face_recognition.face_locations(rgb_image)
            if not face_locations:
                raise Exception("No face detected in image")
                
            face_encoding = face_recognition.face_encodings(rgb_image, face_locations)[0]
            
            # Create face encoding model
            encoding = FaceEncoding.from_numpy(user_id, face_encoding, photo_url)
            
            # Store in database
            response = await cls.supabase.table('face_encodings')\
                .upsert(encoding.dict())\
                .execute()

            # Update user profile with photo URL
            await cls.supabase.table('users')\
                .update({'photo_url': photo_url})\
                .eq('id', str(user_id))\
                .execute()
            
            # Update local cache
            cls.known_face_encodings[user_id] = face_encoding
            
            return {
                'success': True,
                'photo_url': photo_url
            }
            
        except Exception as e:
            raise Exception(f"Error registering face: {str(e)}")