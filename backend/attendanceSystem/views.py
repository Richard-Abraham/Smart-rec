from django.http import JsonResponse
from .utils import handle_request
from .services.auth import AuthService
from .services.face_recognition import FaceRecognitionService
from .services.attendance import AttendanceService

class AuthView:
    @staticmethod
    @handle_request
    async def sign_up(body: dict) -> JsonResponse:
        return await AuthService.sign_up(body)

    @staticmethod
    @handle_request
    async def sign_in(body: dict) -> JsonResponse:
        return await AuthService.sign_in(body)

    @staticmethod
    @handle_request
    async def sign_out(body: dict) -> JsonResponse:
        session_token = body.get('session_token')
        if not session_token:
            raise KeyError('session_token')
        return await AuthService.sign_out(session_token)

    @staticmethod
    @handle_request
    async def get_user_profile(user_id: str) -> JsonResponse:
        profile = await AuthService.get_user_profile(user_id)
        if not profile:
            raise Exception('User profile not found')
        return profile

    @staticmethod
    @handle_request
    async def update_user_profile(body: dict) -> JsonResponse:
        user_id = body.get('user_id')
        profile_data = body.get('profile_data')
        if not user_id or not profile_data:
            raise KeyError('user_id and profile_data are required')
        return await AuthService.update_user_profile(user_id, profile_data)

class FaceRecognitionView:
    @staticmethod
    @handle_request
    async def register_face(body: dict) -> JsonResponse:
        user_id = body.get('user_id')
        image_data = body.get('image_data')
        if not user_id or not image_data:
            raise KeyError('user_id and image_data are required')
        return await FaceRecognitionService.register_face(user_id, image_data)

class AttendanceView:
    @staticmethod
    @handle_request
    async def get_today_records() -> JsonResponse:
        return await AttendanceService.get_today_records()

    @staticmethod
    @handle_request
    async def record_attendance(body: dict) -> JsonResponse:
        user_id = body.get('user_id')
        if not user_id:
            raise KeyError('user_id')
        return await AttendanceService.record_attendance(user_id)

    @staticmethod
    @handle_request
    async def get_attendance_report(body: dict) -> JsonResponse:
        date = body.get('date')
        if not date:
            raise KeyError('date is required')
        return await AttendanceService.get_attendance_report(date)