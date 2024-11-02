from functools import wraps
from django.http import JsonResponse
import json
from asgiref.sync import iscoroutinefunction

def handle_request(view_func):
    """Decorator to handle request processing and response formatting"""
    @wraps(view_func)
    async def wrapper(request, *args, **kwargs):
        try:
            # For POST/PUT/PATCH requests, parse JSON body
            if request.method in ['POST', 'PUT', 'PATCH']:
                body = json.loads(request.body)
                kwargs['body'] = body
            
            response = await view_func(request, *args, **kwargs)
            return JsonResponse({
                'status': 200,
                'message': 'Success',
                'data': response
            })
            
        except json.JSONDecodeError:
            return JsonResponse({
                'status': 400,
                'message': 'Invalid JSON in request body',
                'data': {}
            }, status=400)
        except Exception as e:
            return JsonResponse({
                'status': 500,
                'message': str(e),
                'data': {}
            }, status=500)
    
    return wrapper
