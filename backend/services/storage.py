from supabase import create_client, Client
from django.conf import settings
from typing import Optional
import base64
from .settings import get_env_settings

class StorageService:
    bucket_name = "face-rec"

    @classmethod
    async def _get_client(cls) -> Client:
        """Get or create Supabase client instance"""
        env_settings = get_env_settings()
        return create_client(
            env_settings['SUPABASE_URL'],
            env_settings['SUPABASE_KEY']
        )

    @classmethod
    async def upload_photo(cls, user_id: str, photo_data: str) -> Optional[str]:
        supabase = await cls._get_client()
        try:
            # Decode base64 image
            image_data = base64.b64decode(photo_data.split(',')[1])
            file_path = f"{user_id}/profile.jpg"
            
            # Upload to Supabase Storage
            await supabase.storage.from_(cls.bucket_name).upload(
                file_path,
                image_data
            )
            
            # Get public URL
            url = supabase.storage.from_(cls.bucket_name).get_public_url(file_path)
            return url
        except Exception as e:
            print(f"Error uploading photo: {str(e)}")
            return None 