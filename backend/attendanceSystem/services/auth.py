import uuid
from supabase import create_client, Client
from django.conf import settings
from typing import Dict, Optional
from datetime import datetime
import jwt
from services.storage import StorageService
from models.user import User
from services.settings import get_env_settings

class AuthService:
    @classmethod
    async def _get_client(cls) -> Client:
        """Get or create Supabase client instance"""
        env_settings = get_env_settings()
        return create_client(
            env_settings['SUPABASE_URL'],
            env_settings['SUPABASE_KEY']
        )

    @classmethod
    async def sign_up(cls, request_data: dict) -> Dict:
        """Register a new user with Supabase and create custom user profile"""
        try:
            supabase = await cls._get_client()
            
            # Create auth user
            auth_response = await supabase.auth.sign_up({
                "email": request_data["email"],
                "password": request_data["password"]
            })

            if auth_response.user:
                # Handle photo upload if provided
                photo_url = None
                if "photo" in request_data:
                    photo_url = await StorageService.upload_photo(
                        str(auth_response.user.id), 
                        request_data["photo"]
                    )

                # Create user profile
                user = User(
                    id=auth_response.user.id,  # Use Supabase auth user ID
                    first_name=request_data["first_name"],
                    last_name=request_data["last_name"],
                    photo_url=photo_url,
                    created_at=datetime.utcnow()
                )

                profile_response = await supabase.table("users").insert(user.dict()).execute()

                return {
                    "user": auth_response.user,
                    "access_token": auth_response.session.access_token,
                    "profile": profile_response.data[0] if profile_response.data else None
                }

            raise Exception("Failed to create user")
        except Exception as e:
            raise Exception(f"Sign up failed: {str(e)}")

    @classmethod
    async def sign_in(cls, body: dict) -> Dict:
        """
        Authenticate user with Supabase
        """
        try:
            auth_response = await cls.supabase.auth.sign_in_with_password({
                "email": body["email"],
                "password": body["password"]
            })

            if auth_response.user:
                # Fetch user profile from custom users table
                profile_response = await cls.supabase.table("users")\
                    .select("*")\
                    .eq("id", auth_response.user.id)\
                    .single()\
                    .execute()

                return {
                    "user": auth_response.user,
                    "access_token": auth_response.session.access_token,
                    "profile": profile_response.data if profile_response.data else None,
                    "session": auth_response.session
                }

            raise Exception("Invalid credentials")

        except Exception as e:
            raise Exception(f"Sign in failed: {str(e)}")

    @classmethod
    async def sign_out(cls, session_token: str) -> bool:
        """
        Sign out user and invalidate session
        """
        try:
            await cls.supabase.auth.sign_out(session_token)
            return True
        except Exception as e:
            raise Exception(f"Sign out failed: {str(e)}")

    @classmethod
    def verify_token(cls, token: str) -> Optional[Dict]:
        """
        Verify JWT token and return decoded payload
        """
        try:
            decoded = jwt.decode(
                token,
                settings.SUPABASE_JWT_SECRET,
                algorithms=["HS256"]
            )
            return decoded
        except jwt.InvalidTokenError:
            return None

    @classmethod
    async def get_user_profile(cls, user_id: str) -> Optional[Dict]:
        """
        Fetch user profile from custom users table
        """
        try:
            response = await cls.supabase.table("users")\
                .select("*")\
                .eq("id", user_id)\
                .single()\
                .execute()
            
            return response.data if response.data else None
        except Exception:
            return None

    @classmethod
    async def update_user_profile(cls, user_id: str, profile_data: Dict) -> Optional[Dict]:
        """
        Update user profile in custom users table
        """
        try:
            response = await cls.supabase.table("users")\
                .update(profile_data)\
                .eq("id", user_id)\
                .execute()
            
            return response.data[0] if response.data else None
        except Exception as e:
            raise Exception(f"Profile update failed: {str(e)}")
