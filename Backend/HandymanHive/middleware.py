import jwt
import os
from django.http import JsonResponse
import json

class JWTAuthorizationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.included_paths = ['/edit_personal_profile', '/delete_user', '/get_user_data', '/update_services', '/get_services', '/upload_certificate']  # List of included paths
        self.admin_paths=['/dashboard_view'] # paths for the admin
        self.admin_list=['2021csb1062@iitrpr.ac.in','2021csb1065@iitrpr.ac.in','2021csb1124@iitrpr.ac.in'] #adminlist

    def __call__(self, request):
        response = self.get_response(request)

        # Check if the request path should be included for token validation
        if any(request.path.startswith(path) for path in self.included_paths):
            try:
                data = json.loads(request.body)
                token = data.get('token')
                if not token:
                    return JsonResponse({'error': 'Token not provided'}, status=401)

                payload = jwt.decode(token, os.getenv("Secret_Key"), algorithms=["HS256"])
                request.user_email = payload.get("email")  # Attach decoded payload to request object
                
                # Check if the email from the token matches the provided email
                if request.user_email != payload.get("email"):
                    return JsonResponse({'error': 'Email mismatch'}, status=401)
                if request.path in self.admin_paths and request.user_email not in self.admin_list:
                    return JsonResponse({'error': 'Unauthorized access'}, status=403)
            except jwt.ExpiredSignatureError:
                return JsonResponse({'error': 'Token expired'}, status=401)
            except (jwt.InvalidTokenError, json.JSONDecodeError, KeyError):
                return JsonResponse({'error': 'Invalid token'}, status=401)

        return response
