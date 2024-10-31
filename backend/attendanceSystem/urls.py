"""attendanceSystem URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from attendanceSystem.auth import AuthService
from attendanceSystem.face_recognition import FaceRecognitionService
from attendanceSystem.attendance import AttendanceService
from django.views.decorators.csrf import csrf_exempt
from asgiref.sync import sync_to_async

# Wrapper to call async methods
async def async_view(view_func, *args, **kwargs):
    return await sync_to_async(view_func)(*args, **kwargs)

urlpatterns = [
    path('api/auth/sign-up', csrf_exempt(lambda request: async_view(AuthService.sign_up, request.POST)), name='sign-up'),
    path('api/auth/sign-in', csrf_exempt(lambda request: async_view(AuthService.sign_in, request.POST)), name='sign-in'),
    path('api/auth/sign-out', csrf_exempt(lambda request: async_view(AuthService.sign_out, request.POST)), name='sign-out'),
    path('api/register-face', csrf_exempt(lambda request: async_view(FaceRecognitionService.register_face, request.POST)), name='register-face'),
    path('api/attendance/today', csrf_exempt(lambda request: async_view(AttendanceService.get_today_records)), name='attendance'),
    path('api/attendance/record', csrf_exempt(lambda request: async_view(AttendanceService.record_attendance, request.POST)), name="record-attendance")
]