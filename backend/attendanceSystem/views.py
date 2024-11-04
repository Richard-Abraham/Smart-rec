from django.http import JsonResponse, FileResponse
from django.views.decorators.http import require_http_methods, require_POST, require_GET
from .utils import handle_request, ExportUtils
from .services.auth import AuthService
from .services.face_recognition import FaceRecognitionService
from .services.attendance import AttendanceService
import json
import cv2
import numpy as np
from rest_framework.decorators import api_view
from rest_framework.response import Response
import base64
import time
from .supabase_client import supabase
from datetime import datetime, timezone, timedelta
from django.db.models import Count
from django.db.models.functions import TruncDate
from django.core.mail import send_mail
from django.template.loader import render_to_string

class AuthView:
    @staticmethod
    def sign_up(request):
        try:
            data = json.loads(request.body)
            email = data.get('email')
            password = data.get('password')
            
            # Sign up with Supabase
            response = supabase.auth.sign_up({
                "email": email,
                "password": password
            })
            
            if response.user:
                # Profile will be created automatically by the trigger
                return JsonResponse({
                    'success': True,
                    'message': 'User created successfully',
                    'data': {
                        'id': response.user.id,
                        'email': response.user.email
                    }
                })
            else:
                return JsonResponse({
                    'error': 'Failed to create user'
                }, status=400)
                
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    @staticmethod
    def sign_in(request):
        try:
            data = json.loads(request.body)
            email = data.get('email')
            password = data.get('password')
            
            response = supabase.auth.sign_in_with_password({
                "email": email,
                "password": password
            })
            
            # Get user profile
            profile = supabase.table('profiles').select('*').eq('id', response.user.id).single().execute()
            
            return JsonResponse({
                'success': True,
                'token': response.session.access_token,
                'user': {
                    'id': response.user.id,
                    'email': response.user.email,
                    'profile': profile.data if profile else None
                }
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    @staticmethod
    def sign_out(request):
        try:
            supabase.auth.sign_out()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    @staticmethod
    def get_user_profile(request, user_id):
        try:
            response = supabase.table('profiles').select('*').eq('id', user_id).single().execute()
            return JsonResponse({
                'success': True,
                'data': response.data
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    @staticmethod
    def update_user_profile(request):
        try:
            data = json.loads(request.body)
            user_id = request.user.id
            
            response = supabase.table('profiles').update(data).eq('id', user_id).execute()
            return JsonResponse({
                'success': True,
                'data': response.data
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

class FaceRecognitionView:
    @staticmethod
    def register_face(request):
        try:
            print("Received face registration request")
            
            # Parse JSON data from request body
            try:
                body_data = json.loads(request.body.decode('utf-8'))
                image_data = body_data.get('image')
            except json.JSONDecodeError as e:
                return JsonResponse({'error': 'Invalid JSON data'}, status=400)
            
            if not image_data:
                return JsonResponse({'error': 'No image data provided'}, status=400)

            try:
                # Convert base64 to image
                image_data = image_data.split(',')[1] if ',' in image_data else image_data
                nparr = np.frombuffer(base64.b64decode(image_data), np.uint8)
                image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                
                if image is None:
                    return JsonResponse({'error': 'Invalid image data'}, status=400)
                
            except Exception as e:
                return JsonResponse({'error': f'Image processing error: {str(e)}'}, status=400)

            # Load the face cascade and detect faces
            try:
                face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                
                # Adjust these parameters to make detection more lenient
                # minNeighbors: Lower value = more detections but more false positives
                # scaleFactor: Higher value = faster but might miss faces
                faces = face_cascade.detectMultiScale(
                    gray,
                    scaleFactor=1.3,  # Changed from 1.1
                    minNeighbors=3,   # Changed from 4
                    minSize=(30, 30)  # Minimum face size
                )
                
                print(f"Found {len(faces)} faces")  # Debug print
                
                if len(faces) == 0:
                    return JsonResponse({'error': 'No face detected in image'}, status=400)
                
                # If multiple faces found, use the largest one
                if len(faces) > 1:
                    # Get the face with the largest area
                    largest_face = max(faces, key=lambda rect: rect[2] * rect[3])
                    faces = np.array([largest_face])
                    print(f"Multiple faces found, using largest face")
                
                # Get the face region
                x, y, w, h = faces[0]
                face_image = image[y:y+h, x:x+w]
                
                # Create face encoding
                face_encoding = cv2.mean(face_image)[:3]
                encoding_string = ','.join(map(str, face_encoding))
                
            except Exception as e:
                return JsonResponse({'error': f'Face detection error: {str(e)}'}, status=400)

            try:
                # Get user from request
                auth_header = request.headers.get('Authorization')
                if not auth_header or not auth_header.startswith('Bearer '):
                    return JsonResponse({'error': 'No authorization token'}, status=401)
                
                token = auth_header.split(' ')[1]
                user = supabase.auth.get_user(token)
                
                # Debug print
                print(f"User ID: {user.user.id}")
                
                # No need to verify user - if we got here, the token is valid
                
            except Exception as e:
                print(f"Auth error: {str(e)}")
                return JsonResponse({'error': f'Authentication error: {str(e)}'}, status=401)

            try:
                # Upload image to Supabase storage
                _, buffer = cv2.imencode('.jpg', image)
                file_name = f"faces/{user.user.id}_{int(time.time())}.jpg"
                
                storage_response = supabase.storage.from_('face-photos').upload(
                    file_name,
                    buffer.tobytes(),
                    {'content-type': 'image/jpeg'}
                )
                
                # Get public URL
                public_url = supabase.storage.from_('face-photos').get_public_url(file_name)
                
                # Debug print before insert
                print(f"About to insert record for user {user.user.id}")
                print(f"Encoding string length: {len(encoding_string)}")
                print(f"Public URL: {public_url}")
                
                # Create face encoding record
                face_record = supabase.table('face_encodings').insert({
                    'user_id': user.user.id,  # Supabase will handle the UUID conversion
                    'photo_url': public_url,
                    'encoding': encoding_string,
                    'is_active': True
                }).execute()
                
                print("Record inserted successfully")
                
                return JsonResponse({
                    'success': True,
                    'message': 'Face registered successfully',
                    'data': {
                        'photo_url': public_url,
                        'record': face_record.data
                    }
                })
                
            except Exception as e:
                print(f"Storage/DB error: {str(e)}")
                print(f"Error type: {type(e)}")
                return JsonResponse({'error': f'Storage/Database error: {str(e)}'}, status=500)

        except Exception as e:
            print(f"General error: {str(e)}")
            return JsonResponse({'error': str(e)}, status=500)

    @staticmethod
    def verify_face(request):
        try:
            # Get image from request
            body_data = json.loads(request.body.decode('utf-8'))
            image_data = body_data.get('image')
            
            # Convert base64 to image
            image_data = image_data.split(',')[1] if ',' in image_data else image_data
            nparr = np.frombuffer(base64.b64decode(image_data), np.uint8)
            image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            
            # Detect face
            face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 3, minSize=(30, 30))
            
            if len(faces) == 0:
                return JsonResponse({'error': 'No face detected'}, status=400)
            
            # Get largest face
            largest_face = max(faces, key=lambda rect: rect[2] * rect[3])
            x, y, w, h = largest_face
            face_image = image[y:y+h, x:x+w]
            
            # Create face encoding
            face_encoding = cv2.mean(face_image)[:3]
            encoding_to_verify = ','.join(map(str, face_encoding))
            
            # Get user's registered face encoding
            auth_header = request.headers.get('Authorization')
            token = auth_header.split(' ')[1]
            user = supabase.auth.get_user(token)
            
            registered_face = supabase.table('face_encodings')\
                .select('*')\
                .eq('user_id', user.user.id)\
                .eq('is_active', True)\
                .order('created_at.desc')\
                .limit(1)\
                .execute()
            
            if not registered_face.data:
                return JsonResponse({'error': 'No registered face found'}, status=404)
            
            # Compare encodings
            registered_encoding = [float(x) for x in registered_face.data[0]['encoding'].split(',')]
            tolerance = 50  # Adjust this value based on testing
            
            differences = [abs(a - b) for a, b in zip(registered_encoding, face_encoding)]
            average_difference = sum(differences) / len(differences)
            
            if average_difference <= tolerance:
                return JsonResponse({
                    'success': True,
                    'message': 'Face verified successfully',
                    'confidence': 1 - (average_difference / tolerance)
                })
            else:
                return JsonResponse({
                    'success': False,
                    'message': 'Face verification failed',
                    'confidence': 1 - (average_difference / tolerance)
                }, status=401)
                
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

class AttendanceView:
    @staticmethod
    @handle_request
    @require_GET
    async def get_today_records() -> JsonResponse:
        return await AttendanceService.get_today_records()

    @staticmethod
    @handle_request
    @require_POST
    async def record_attendance(body: dict) -> JsonResponse:
        user_id = body.get('user_id')
        if not user_id:
            raise KeyError('user_id')
        return await AttendanceService.record_attendance(user_id)

    @staticmethod
    @handle_request
    @require_GET
    async def get_attendance_report(request) -> JsonResponse:
        date = request.GET.get('date')
        if not date:
            raise KeyError('date is required')
        return await AttendanceService.get_attendance_report(date)

    @staticmethod
    def check_in(request):
        try:
            # Get image from request
            body_data = json.loads(request.body.decode('utf-8'))
            image_data = body_data.get('image')
            
            # Convert base64 to image
            image_data = image_data.split(',')[1] if ',' in image_data else image_data
            nparr = np.frombuffer(base64.b64decode(image_data), np.uint8)
            image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            
            # Detect face
            face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 3, minSize=(30, 30))
            
            if len(faces) == 0:
                return JsonResponse({'error': 'No face detected'}, status=400)
            
            # Get largest face
            largest_face = max(faces, key=lambda rect: rect[2] * rect[3])
            x, y, w, h = largest_face
            face_image = image[y:y+h, x:x+w]
            
            # Create face encoding
            face_encoding = cv2.mean(face_image)[:3]
            encoding_to_verify = ','.join(map(str, face_encoding))
            
            # Get user
            auth_header = request.headers.get('Authorization')
            token = auth_header.split(' ')[1]
            user = supabase.auth.get_user(token)
            
            # Get registered face
            registered_face = supabase.table('face_encodings')\
                .select('*')\
                .eq('user_id', user.user.id)\
                .eq('is_active', True)\
                .order('created_at.desc')\
                .limit(1)\
                .execute()
            
            if not registered_face.data:
                return JsonResponse({'error': 'No registered face found'}, status=404)
            
            # Compare encodings
            registered_encoding = [float(x) for x in registered_face.data[0]['encoding'].split(',')]
            tolerance = 50
            
            differences = [abs(a - b) for a, b in zip(registered_encoding, face_encoding)]
            average_difference = sum(differences) / len(differences)
            confidence = 1 - (average_difference / tolerance)
            
            if confidence > 0.6:  # 60% confidence threshold
                # Check if already checked in today
                today = datetime.now(timezone.utc)
                existing_attendance = supabase.table('attendance')\
                    .select('*')\
                    .eq('user_id', user.user.id)\
                    .is_('check_out', 'null')\
                    .execute()
                
                if existing_attendance.data:
                    return JsonResponse({
                        'success': False,
                        'message': 'Already checked in',
                        'data': existing_attendance.data[0]
                    })
                
                # Create attendance record
                attendance = supabase.table('attendance').insert({
                    'user_id': user.user.id,
                    'confidence': float(confidence),
                    'status': 'present'
                }).execute()
                
                return JsonResponse({
                    'success': True,
                    'message': 'Check-in successful',
                    'data': attendance.data[0]
                })
            else:
                return JsonResponse({
                    'success': False,
                    'message': 'Face verification failed',
                    'confidence': confidence
                }, status=401)
                
        except Exception as e:
            print(f"Check-in error: {str(e)}")
            return JsonResponse({'error': str(e)}, status=500)
    
    @staticmethod
    def check_out(request):
        try:
            # Similar face verification process as check_in
            # ... (face detection and verification code) ...
            
            # Get user
            auth_header = request.headers.get('Authorization')
            token = auth_header.split(' ')[1]
            user = supabase.auth.get_user(token)
            
            # Find active check-in
            active_attendance = supabase.table('attendance')\
                .select('*')\
                .eq('user_id', user.user.id)\
                .is_('check_out', 'null')\
                .execute()
            
            if not active_attendance.data:
                return JsonResponse({
                    'success': False,
                    'message': 'No active check-in found'
                }, status=404)
            
            # Update check-out time
            attendance = supabase.table('attendance')\
                .update({'check_out': datetime.now(timezone.utc).isoformat()})\
                .eq('id', active_attendance.data[0]['id'])\
                .execute()
            
            return JsonResponse({
                'success': True,
                'message': 'Check-out successful',
                'data': attendance.data[0]
            })
            
        except Exception as e:
            print(f"Check-out error: {str(e)}")
            return JsonResponse({'error': str(e)}, status=500)

    @staticmethod
    def get_history(request):
        try:
            # Get user
            auth_header = request.headers.get('Authorization')
            token = auth_header.split(' ')[1]
            user = supabase.auth.get_user(token)
            
            # Get query parameters
            params = request.GET
            period = params.get('period', 'week')  # week, month, or all
            
            # Calculate date range
            end_date = datetime.now(timezone.utc)
            if period == 'week':
                start_date = end_date - timedelta(days=7)
            elif period == 'month':
                start_date = end_date - timedelta(days=30)
            else:
                start_date = end_date - timedelta(days=365)  # Get up to a year of history
            
            # Query attendance records
            attendance = supabase.table('attendance')\
                .select('*')\
                .eq('user_id', user.user.id)\
                .gte('created_at', start_date.isoformat())\
                .lte('created_at', end_date.isoformat())\
                .order('created_at', desc=True)\
                .execute()
            
            # Calculate statistics
            total_hours = 0
            late_days = 0
            early_departures = 0
            work_start_time = time(9, 0)  # 9:00 AM
            work_end_time = time(17, 0)   # 5:00 PM
            
            for record in attendance.data:
                check_in_time = datetime.fromisoformat(record['check_in'].replace('Z', '+00:00'))
                if record['check_out']:
                    check_out_time = datetime.fromisoformat(record['check_out'].replace('Z', '+00:00'))
                    duration = (check_out_time - check_in_time).total_seconds() / 3600  # hours
                    total_hours += duration
                    
                    if check_out_time.time() < work_end_time:
                        early_departures += 1
                
                if check_in_time.time() > work_start_time:
                    late_days += 1
            
            stats = {
                'total_hours': round(total_hours, 2),
                'late_days': late_days,
                'early_departures': early_departures,
                'total_days': len(attendance.data),
                'attendance_rate': round(len(attendance.data) / 7 * 100, 2) if period == 'week' else 
                                 round(len(attendance.data) / 30 * 100, 2) if period == 'month' else 0
            }
            
            return JsonResponse({
                'success': True,
                'data': attendance.data,
                'stats': stats
            })
            
        except Exception as e:
            print(f"History error: {str(e)}")
            return JsonResponse({'error': str(e)}, status=500)

    @staticmethod
    def get_report(request):
        try:
            # Get user and verify admin status
            auth_header = request.headers.get('Authorization')
            token = auth_header.split(' ')[1]
            user = supabase.auth.get_user(token)
            
            # Get query parameters
            params = request.GET
            start_date = params.get('start_date')
            end_date = params.get('end_date')
            report_type = params.get('type', 'daily')  # daily, weekly, monthly
            
            if not start_date or not end_date:
                return JsonResponse({'error': 'Start date and end date are required'}, status=400)
            
            # Query attendance records
            query = supabase.table('attendance')\
                .select('*, profiles(full_name, email)')\
                .gte('created_at', start_date)\
                .lte('created_at', end_date)
            
            if report_type == 'daily':
                query = query.order('created_at', desc=True)
            
            attendance = query.execute()
            
            # Process data based on report type
            if report_type == 'daily':
                report_data = attendance.data
            else:
                # Group by user and calculate statistics
                report_data = {}
                for record in attendance.data:
                    user_id = record['user_id']
                    if user_id not in report_data:
                        report_data[user_id] = {
                            'user': record['profiles'],
                            'total_hours': 0,
                            'late_days': 0,
                            'early_departures': 0,
                            'total_days': 0
                        }
                    
                    # Calculate statistics similar to get_history
                    # ... (statistics calculation code) ...
                
                report_data = list(report_data.values())
            
            return JsonResponse({
                'success': True,
                'report_type': report_type,
                'data': report_data
            })
            
        except Exception as e:
            print(f"Report error: {str(e)}")
            return JsonResponse({'error': str(e)}, status=500)

class AdminView:
    @staticmethod
    def is_admin(user_id):
        try:
            result = supabase.rpc('is_admin', {'user_id': user_id}).execute()
            return result.data
        except Exception:
            return False

    @staticmethod
    def admin_required(view_func):
        def wrapped_view(request, *args, **kwargs):
            try:
                auth_header = request.headers.get('Authorization')
                if not auth_header or not auth_header.startswith('Bearer '):
                    return JsonResponse({'error': 'No authorization token'}, status=401)
                
                token = auth_header.split(' ')[1]
                user = supabase.auth.get_user(token)
                
                if not AdminView.is_admin(user.user.id):
                    return JsonResponse({'error': 'Admin access required'}, status=403)
                
                return view_func(request, *args, **kwargs)
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=401)
        return wrapped_view

    @staticmethod
    @admin_required
    def get_dashboard_stats(request):
        try:
            # Get date range
            end_date = datetime.now(timezone.utc)
            start_date = end_date - timedelta(days=30)
            
            # Get all attendance records
            attendance = supabase.table('attendance')\
                .select('*, profiles(full_name, email)')\
                .gte('created_at', start_date.isoformat())\
                .lte('created_at', end_date.isoformat())\
                .execute()
            
            # Calculate statistics
            total_employees = len(set(record['user_id'] for record in attendance.data))
            total_hours = sum(
                (datetime.fromisoformat(record['check_out'].replace('Z', '+00:00')) - 
                 datetime.fromisoformat(record['check_in'].replace('Z', '+00:00'))).total_seconds() / 3600
                for record in attendance.data if record['check_out']
            )
            late_arrivals = sum(1 for record in attendance.data 
                              if datetime.fromisoformat(record['check_in'].replace('Z', '+00:00')).time() > time(9, 15))
            
            return JsonResponse({
                'success': True,
                'stats': {
                    'total_employees': total_employees,
                    'total_hours': round(total_hours, 2),
                    'late_arrivals': late_arrivals,
                    'attendance_records': len(attendance.data)
                },
                'recent_attendance': attendance.data[:10]  # Last 10 records
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    @staticmethod
    @admin_required
    def manage_employees(request):
        if request.method == 'GET':
            try:
                employees = supabase.table('profiles')\
                    .select('*, admin_roles(role)')\
                    .execute()
                
                return JsonResponse({
                    'success': True,
                    'data': employees.data
                })
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=500)
        
        elif request.method == 'POST':
            try:
                data = json.loads(request.body)
                action = data.get('action')
                user_id = data.get('user_id')
                
                if action == 'make_admin':
                    supabase.table('admin_roles').upsert({
                        'user_id': user_id,
                        'role': 'admin'
                    }).execute()
                elif action == 'remove_admin':
                    supabase.table('admin_roles')\
                        .delete()\
                        .eq('user_id', user_id)\
                        .execute()
                
                return JsonResponse({'success': True})
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=500)

    @staticmethod
    def send_notification(user_email, subject, template_name, context):
        try:
            html_message = render_to_string(template_name, context)
            send_mail(
                subject=subject,
                message='',
                html_message=html_message,
                from_email='your-email@example.com',
                recipient_list=[user_email],
                fail_silently=False,
            )
            return True
        except Exception as e:
            print(f"Email error: {str(e)}")
            return False

    @staticmethod
    def check_late_arrivals():
        try:
            # Get settings
            settings = supabase.table('admin_settings')\
                .select('*')\
                .eq('setting_key', 'work_hours')\
                .single()\
                .execute()
            
            work_hours = settings.data['setting_value']
            start_time = datetime.strptime(work_hours['start'], '%H:%M').time()
            grace_period = timedelta(minutes=work_hours['grace_period'])
            
            # Get today's attendance
            today = datetime.now(timezone.utc)
            attendance = supabase.table('attendance')\
                .select('*, profiles(email, full_name)')\
                .gte('created_at', today.date().isoformat())\
                .execute()
            
            # Check for late arrivals
            for record in attendance.data:
                check_in = datetime.fromisoformat(record['check_in'].replace('Z', '+00:00'))
                if check_in.time() > (datetime.combine(today.date(), start_time) + grace_period).time():
                    # Send notification
                    AdminView.send_notification(
                        user_email=record['profiles']['email'],
                        subject='Late Arrival Notice',
                        template_name='emails/late_arrival.html',
                        context={
                            'name': record['profiles']['full_name'],
                            'check_in_time': check_in.strftime('%I:%M %p'),
                            'expected_time': start_time.strftime('%I:%M %p')
                        }
                    )
            
            return True
        except Exception as e:
            print(f"Late check error: {str(e)}")
            return False

class ReportView:
    @staticmethod
    def generate_detailed_report(request):
        try:
            # Get parameters
            params = request.GET
            start_date = params.get('start_date')
            end_date = params.get('end_date')
            report_type = params.get('type', 'daily')  # daily, weekly, monthly
            format = params.get('format', 'json')  # json, excel, pdf
            
            # Base query
            query = supabase.table('attendance')\
                .select('*, profiles(full_name, email)')\
                .gte('created_at', start_date)\
                .lte('created_at', end_date)
            
            # Execute query
            result = query.execute()
            
            # Process data
            data = result.data
            
            # Calculate statistics
            stats = {
                'total_records': len(data),
                'unique_employees': len(set(r['user_id'] for r in data)),
                'total_hours': sum(
                    (datetime.fromisoformat(r['check_out'].replace('Z', '+00:00')) - 
                     datetime.fromisoformat(r['check_in'].replace('Z', '+00:00'))).total_seconds() / 3600
                    for r in data if r['check_out']
                ),
                'late_arrivals': sum(
                    1 for r in data 
                    if datetime.fromisoformat(r['check_in'].replace('Z', '+00:00')).time() > time(9, 15)
                )
            }
            
            # Format data based on report type
            if report_type == 'weekly':
                # Group by week
                weekly_data = {}
                for record in data:
                    week = datetime.fromisoformat(record['check_in'].replace('Z', '+00:00')).strftime('%Y-W%W')
                    if week not in weekly_data:
                        weekly_data[week] = {
                            'week': week,
                            'total_hours': 0,
                            'late_arrivals': 0,
                            'attendance_count': 0
                        }
                    
                    weekly_data[week]['attendance_count'] += 1
                    if record['check_out']:
                        duration = (datetime.fromisoformat(record['check_out'].replace('Z', '+00:00')) - 
                                  datetime.fromisoformat(record['check_in'].replace('Z', '+00:00'))).total_seconds() / 3600
                        weekly_data[week]['total_hours'] += duration
                    
                    if datetime.fromisoformat(record['check_in'].replace('Z', '+00:00')).time() > time(9, 15):
                        weekly_data[week]['late_arrivals'] += 1
                
                data = list(weekly_data.values())
            
            # Generate response based on format
            if format == 'excel':
                output = ExportUtils.generate_excel(data, f'attendance_report_{report_type}.xlsx')
                return FileResponse(
                    output,
                    as_attachment=True,
                    filename=f'attendance_report_{report_type}.xlsx'
                )
            
            elif format == 'pdf':
                output = ExportUtils.generate_pdf(
                    data,
                    f'Attendance Report ({report_type.title()})'
                )
                return FileResponse(
                    output,
                    as_attachment=True,
                    filename=f'attendance_report_{report_type}.pdf'
                )
            
            else:
                return JsonResponse({
                    'success': True,
                    'stats': stats,
                    'data': data
                })
                
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
