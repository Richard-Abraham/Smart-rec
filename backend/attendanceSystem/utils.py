from functools import wraps
from typing import Callable, Any
from django.http import JsonResponse
import json
from aiohttp import web

def create_response(status: int, message: str, data: Any = None) -> JsonResponse:
    return JsonResponse({
        'status': status,
        'message': message,
        'data': data if data is not None else {}
    }, status=status)

def handle_request(func: Callable) -> Callable:
    @wraps(func)
    async def wrapper(request: web.Request, *args: Any, **kwargs: Any) -> JsonResponse:
        try:
            # Parse request body for POST requests
            if request.method == 'POST':
                body = await request.json() if request.content_type == 'application/json' else await request.post()
                result = await func(body, *args, **kwargs)
            else:
                result = await func(*args, **kwargs)
            
            return create_response(200, 'Success', result)
            
        except json.JSONDecodeError:
            return create_response(400, 'Invalid JSON format')
        except KeyError as e:
            return create_response(400, f'Missing required field: {str(e)}')
        except Exception as e:
            return create_response(500, str(e))
    
    return wrapper