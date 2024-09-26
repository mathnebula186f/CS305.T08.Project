from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from ..models import (
    CustomUser,
    CustomWorker,
    Request,
)
import json

adminlist=["2021csb1062@iitrpr.ac.in","2021csb1124@iitrpr.ac.in","alankritkadian@gmail.com"]


@csrf_exempt
def dashboard_view(request):
    # Count number of users
    num_users = CustomUser.objects.count()

    # Count number of workers
    num_workers = CustomWorker.objects.count()

    # Count number of verified workers
    num_verified_workers = CustomWorker.objects.filter(verified=True).count()

    # Count number of completed tasks
    num_completed_tasks = Request.objects.filter(status='Completed').count()

    data = {
        'num_users': num_users,
        'num_workers': num_workers,
        'num_verified_workers': num_verified_workers,
        'num_completed_tasks': num_completed_tasks
    }
    return JsonResponse(data)

@csrf_exempt
def change_verification_status(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get("email")
        if email:
            try:
                worker = CustomWorker.objects.get(email=email)
                worker.verified = not worker.verified  # Reverse the verification status
                worker.save()
                return JsonResponse({"message": "Verification status changed successfully"})
            except CustomWorker.DoesNotExist:
                return JsonResponse({"error": "Worker not found"}, status=404)
        else:
            return JsonResponse({"error": "Email not provided"}, status=400)
    else:
        return JsonResponse({"error": "Method not allowed"}, status=405)
    
    
@csrf_exempt
def index(request):
    return JsonResponse({"message": "Welcome to HandymanHive!"})
