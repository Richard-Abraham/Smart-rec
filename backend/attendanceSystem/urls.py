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
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from .views import AuthView, FaceRecognitionView, AttendanceView

urlpatterns = [
    path('api/auth/sign-up', 
        csrf_exempt(AuthView.sign_up), 
        name='sign-up'
    ),
    path('api/auth/sign-in', 
        csrf_exempt(AuthView.sign_in), 
        name='sign-in'
    ),
    path('api/auth/sign-out', 
        csrf_exempt(AuthView.sign_out), 
        name='sign-out'
    ),
    path('api/auth/profile/<str:user_id>', 
        csrf_exempt(AuthView.get_user_profile), 
        name='get-profile'
    ),
    path('api/auth/profile/update', 
        csrf_exempt(AuthView.update_user_profile), 
        name='update-profile'
    ),
    path('api/register-face', 
        csrf_exempt(FaceRecognitionView.register_face), 
        name='register-face'
    ),
    path('api/attendance/today', 
        csrf_exempt(AttendanceView.get_today_records), 
        name='attendance'
    ),
    path('api/attendance/record', 
        csrf_exempt(AttendanceView.record_attendance), 
        name='record-attendance'
    ),
    path('api/attendance/report', 
        csrf_exempt(AttendanceView.get_attendance_report), 
        name='attendance-report'
    ),
]