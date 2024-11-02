from supabase import create_client, Client
from django.conf import settings
from typing import Optional
import base64

class StorageService:
    def __init__(self):
        self.supabase: Client = create_client(
            settings.SUPABASE_URL,
            settings.SUPABASE_KEY
        )
        self.bucket_name = 'user-photos'

    async def upload_photo(self, user_id: str, photo_data: str) -> Optional[str]:
        try:
            # Decode base64 image
            image_data = base64.b64decode(photo_data.split(',')[1])
            file_path = f"{user_id}/profile.jpg"
            
            # Upload to Supabase Storage
            await self.supabase.storage.from_(self.bucket_name).upload(
                file_path,
                image_data
            )
            
            # Get public URL
            url = self.supabase.storage.from_(self.bucket_name).get_public_url(file_path)
            return url
        except Exception as e:
            print(f"Error uploading photo: {str(e)}")
            return None 