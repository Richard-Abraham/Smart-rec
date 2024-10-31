from supabase import create_client, Client
from django.conf import settings
from typing import Dict, Optional
from datetime import datetime
import jwt

class AuthService:
    def __init__(self):
        self.supabase: Client = create_client(
            settings.SUPABASE_URL,
            settings.SUPABASE_KEY
        )

    @classmethod
    async def sign_up(cls, user_data: Dict) -> Dict:
        """
        Register a new user with Supabase and create custom user profile
        """
        try:
            # Create auth user in Supabase
            auth_response = await cls.supabase.auth.sign_up({
                "email": user_data["email"],
                "password": user_data["password"]
            })

            if auth_response.user:
                # Create user profile in custom users table
                profile_data = {
                    "id": auth_response.user.id,
                    "email": user_data["email"],
                    "employee_id": user_data["employee_id"],
                    "department": user_data["department"],
                    "first_name": user_data.get("first_name", ""),
                    "last_name": user_data.get("last_name", ""),
                    "created_at": datetime.utcnow().isoformat()
                }

                profile_response = await cls.supabase.table("users").insert(profile_data).execute()

                return {
                    "user": auth_response.user,
                    "profile": profile_response.data[0] if profile_response.data else None
                }
            
            raise Exception("Failed to create user")

        except Exception as e:
            raise Exception(f"Sign up failed: {str(e)}")

    @classmethod
    async def sign_in(cls, email: str, password: str) -> Dict:
        """
        Authenticate user with Supabase
        """
        try:
            auth_response = await cls.supabase.auth.sign_in_with_password({
                "email": email,
                "password": password
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