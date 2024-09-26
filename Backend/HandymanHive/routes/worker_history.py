import datetime
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from ..models import (
    CustomUser,
    CustomWorker,
    Certification,
    WorkerDetails,
    Request,
    WorkHistory,
)
import json
from .notifications import send_notfication

from django.core.exceptions import ObjectDoesNotExist
###################### REQUEST PAGE ROUTES #############################


@csrf_exempt
def get_worker_profile(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email')
            worker_email = data.get('worker_email')

            try:
                worker = CustomWorker.objects.get(email=worker_email)
                worker_details = WorkerDetails.objects.get(email=worker_email)
            except ObjectDoesNotExist:
                return JsonResponse({"error": "Worker not found"}, status=404)

            services_offered = worker_details.services_offered.all()
            services = [service.name for service in services_offered]

            certifications = []
            cert = Certification.objects.filter(worker_email=worker_email)
            for certification in cert:
                certifications.append((certification.certificate_name, certification.issuing_authority))

            return JsonResponse({
                "first_name": worker.first_name,
                "last_name": worker.last_name,
                "email": worker.email,
                "phone_number": worker.phone_number,
                "age": worker.age,
                "years_of_exp": worker_details.years_of_experience,
                "services": services,
                "certification": certifications,
                "verified": worker.verified,
                "address": worker.address,
                "state": worker.state,
                "latitude": worker_details.liveLatitude,
                "longitude": worker_details.liveLongitude,
            })
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data in request body"}, status=400)
        except Exception as e:
            print(e)  # Log the exception for debugging purposes
            return JsonResponse({"error": "Error fetching worker profile"}, status=500)

    else:
        return JsonResponse({"error": "Invalid request method"}, status=400)


@csrf_exempt
def create_request(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)

            user_email = data.get('user_email')
            worker_email = data.get('worker_email')
            service = data.get('service')

            if not all([user_email, worker_email, service]):
                raise KeyError("Missing required fields")

            # Check if the user and worker exist
            user = CustomUser.objects.get(email=user_email)
            worker = CustomWorker.objects.get(email=worker_email)

            if Request.objects.filter(user=user, worker=worker, service=service, status= "Pending").exists():
                return JsonResponse({'status': 'error', 'message': 'Request already exists'})
            
            Request.objects.create(
                user=user,
                worker=worker,
                service=service,
                created_on=timezone.now(),
            )

            send_notfication("Request Work", worker, {"service": service, "user": user.first_name})
            return JsonResponse({'status': 'success', 'message': 'Request created successfully'})

        except json.JSONDecodeError:
            return JsonResponse({"status": "error", "message": "Invalid JSON data in request body"}, status=400)

        except KeyError as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)

        except CustomUser.DoesNotExist:
            return JsonResponse({"status": "error", "message": "User does not exist"}, status=404)

        except CustomWorker.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Worker does not exist"}, status=404)


        except Exception as e:
            print(e)
            return JsonResponse({"status": "error", "message": "Error creating request"}, status=500)

    else:
        return JsonResponse({"status": "error", "message": "Only POST requests are allowed"}, status=405)


@csrf_exempt
def update_request(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user_email = data.get("user_email")
            worker_email = data.get("worker_email")

            # Check if required fields are present
            if not all([user_email, worker_email, "service", "status"]):
                raise KeyError("Missing required fields")

            # Get user and worker objects
            user = CustomUser.objects.get(email=user_email)
            worker = CustomWorker.objects.get(email=worker_email)
            service = data.get("service")
            status = data.get("status")

            # Retrieve the request object
            try:
                request_obj = Request.objects.get(user=user, worker=worker, service=service)
            except ObjectDoesNotExist:
                return JsonResponse({"error": "Request not found"}, status=404)

            # Delete the request
            request_obj.delete()

            # Handle "Accept" status
            if status == "Accept":
                WorkHistory.objects.create(
                    user=user,
                    worker=worker,
                    service=service,
                    started_on=timezone.now(),
                )
                send_notfication("Accepted Work", user, {"service": service, "user": worker.first_name})

            return JsonResponse({"message": "Request deleted and added to WorkHistory successfully"})

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data in request body"}, status=400)

        except KeyError as e:
            return JsonResponse({"error": str(e)}, status=400)

        except ObjectDoesNotExist:
            return JsonResponse({"error": "User or worker does not exist"}, status=404)

        except Exception as e:
            print(e)  # Log the exception for debugging purposes
            return JsonResponse({"error": "Error updating request"}, status=500)

    else:
        return JsonResponse({"error": "Invalid request method"}, status=400)


@csrf_exempt
def get_user_requests(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email')

            # Check if email is provided
            if not email:
                raise KeyError("Email is required")

            # Retrieve the worker object
            try:
                worker = CustomWorker.objects.get(email=email)
            except ObjectDoesNotExist:
                return JsonResponse({'error': 'Worker not found'}, status=404)

            # Retrieve requests for the worker
            requests = Request.objects.filter(worker=worker, status='Pending')

            user_requests = []
            for req in requests:
                user = req.user
                user_requests.append({
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'email': user.email,
                    'service': req.service,
                    'created_on': req.created_on,
                    'status': req.status
                })
            return JsonResponse({'requests': user_requests})

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data in request body'}, status=400)

        except KeyError as e:
            return JsonResponse({'error': str(e)}, status=400)

        except Exception as e:
            print(e)  # Log the exception for debugging purposes
            return JsonResponse({'error': 'Error fetching requests'}, status=500)

    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)


########################### WORKER HISTORY ROUTES #############################


@csrf_exempt
def get_worker_history(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            email = data.get("email")

            if not email:
                raise KeyError("Missing 'email' field in request")

            # Check if the worker exists
            worker = CustomWorker.objects.get(email=email)

            # Fetch done and in-progress works for the worker
            done_works = []
            progress_works = []

            doneWorks = WorkHistory.objects.filter(worker=worker, status="Done")
            for work in doneWorks:
                done_works.append({
                    "first_name": work.user.first_name,
                    "last_name": work.user.last_name,
                    "email": work.user.email,
                    "service": work.service,
                    "started_on": work.started_on,
                    "done_on": work.done_on,
                    "status": "Done",
                    "showingStatus": "Done"
                })

            progressWorks = WorkHistory.objects.filter(worker=worker, status="In Progress")
            for work in progressWorks:
                status = 'In Progress'
                if work.workerdone:
                    status = 'Done'

                progress_works.append({
                    "first_name": work.user.first_name,
                    "last_name": work.user.last_name,
                    "email": work.user.email,
                    "service": work.service,
                    "started_on": work.started_on,
                    "status": status,
                    "showingStatus": status
                })

            return JsonResponse({"progress_works": progress_works, "done_works": done_works})

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data in request body"}, status=400)

        except KeyError as e:
            return JsonResponse({"error": str(e)}, status=400)

        except CustomWorker.DoesNotExist:
            return JsonResponse({"error": "Worker not found"}, status=404)

        except Exception as e:
            return JsonResponse({"error": f"Error fetching work history: {str(e)}"}, status=500)

    else:
        return JsonResponse({"error": "Invalid request method"}, status=400)

@csrf_exempt
def get_user_history(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get("email")

            if not email:
                raise KeyError("Missing 'email' field in request")

            # Check if the user exists
            user = CustomUser.objects.get(email=email)

            # Fetch done and in-progress works for the user
            done_works = []
            progress_works = []

            doneWorks = WorkHistory.objects.filter(user=user, status="Done")
            for work in doneWorks:
                done_works.append({
                    "first_name": work.worker.first_name,
                    "last_name": work.worker.last_name,
                    "email": work.worker.email,
                    "service": work.service,
                    "started_on": work.started_on,
                    "done_on": work.done_on,
                    "status": "Done",
                    "showingStatus": "Done"
                })

            progressWorks = WorkHistory.objects.filter(user=user, status="In Progress")
            for work in progressWorks:
                showingStatus="In Progress"
                status = 'In Progress'
                if work.userdone:
                    showingStatus = 'Done'

                progress_works.append({
                    "first_name": work.worker.first_name,
                    "last_name": work.worker.last_name,
                    "email": work.worker.email,
                    "service": work.service,
                    "started_on": work.started_on,
                    "status": status,
                    "showingStatus": showingStatus,
                })

            return JsonResponse({"progress_works": progress_works, "done_works": done_works})

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data in request body"}, status=400)

        except KeyError as e:
            return JsonResponse({"error": str(e)}, status=400)

        except CustomUser.DoesNotExist:
            return JsonResponse({"error": "User not found"}, status=404)

        except Exception as e:
            return JsonResponse({"error": f"Error fetching user history: {str(e)}"}, status=500)

    else:
        return JsonResponse({"error": "Invalid request method"}, status=400)

@csrf_exempt
def update_user_works(request):
    if request.method == 'POST':        
        try:
            request_data = json.loads(request.body)
            user_email = request_data.get('user_email')
            worker_email = request_data.get('worker_email')
            service = request_data.get('service')
            status = request_data.get('status')
            user_review = request_data.get('user_review')
            user_rating = request_data.get('user_rating')

            if not all([user_email, worker_email, service, status]):
                raise KeyError("Missing required fields")

            # Check if the user and worker exist
            user = CustomUser.objects.get(email=user_email)
            worker = CustomWorker.objects.get(email=worker_email)

            # Retrieve the work
            work = WorkHistory.objects.get(user=user, worker=worker, service=service,status="In Progress")

            if status == 'Reject':
                if work.status != 'In Progress':
                    raise ValueError("Work is not in progress, cannot reject")

                work.delete()
                return JsonResponse({'message': 'Work deleted successfully'})

            if status == 'Done':
                if work.status != 'In Progress':
                    raise ValueError("Work is not in progress, cannot mark as done")

                work.userdone = True
                work.user_done_on = timezone.now()
                work.user_review = user_review
                work.user_rating = user_rating

                if work.workerdone:
                    work.done_on = timezone.now()
                    work.status = 'Done'

                work.save()

                worker_details = WorkerDetails.objects.get(email=worker_email)
                time_str = timezone.now().strftime("%Y-%m-%d %H:%M:%S")

                worker_details.customer_reviews.append({
                    "user": user.first_name,
                    "rating": user_rating,
                    "service": service,
                    "review": user_review,
                    "time": time_str
                })

                worker_details.save()

                sum=0
                counter=0

                for review in worker_details.customer_reviews:
                    sum+=review['rating']
                    counter+=1

                worker_details.overall_rating=sum/counter

                print("here is the overall rating=",worker_details.overall_rating,sum/counter)

                worker_details.save()

                return JsonResponse({'message': 'Work accepted successfully'})

            return JsonResponse({'message': 'Status updated successfully'})

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data in request body'}, status=400)

        except KeyError as e:
            return JsonResponse({'error': f"Missing field: {str(e)}"}, status=400)

        except CustomUser.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)

        except CustomWorker.DoesNotExist:
            return JsonResponse({'error': 'Worker not found'}, status=404)

        except WorkHistory.DoesNotExist:
            return JsonResponse({'error': 'Work history not found'}, status=404)

        except ValueError as e:
            return JsonResponse({'error': str(e)}, status=400)

        except Exception as e:
            print(e)
            return JsonResponse({'error': 'Error updating the status'}, status=500)

    else:
        return JsonResponse({"error": "Invalid request method"}, status=400)

@csrf_exempt
def update_worker_works(request):
    if request.method == 'POST':
        try:
            request_data = json.loads(request.body)
            user_email = request_data.get('user_email')
            worker_email = request_data.get('worker_email')
            service = request_data.get('service')
            status = request_data.get('status')

            if not all([user_email, worker_email, service, status]):
                raise KeyError("Missing required fields")

            # Check if the user and worker exist
            user = CustomUser.objects.get(email=user_email)
            worker = CustomWorker.objects.get(email=worker_email)
            # Retrieve the work
            work = WorkHistory.objects.get(
                user=user, worker=worker, service=service, status="In Progress"
            )
            print("ggggggnu")
            if status == 'Reject':
                if work.status != 'In Progress':
                    raise ValueError("Work is not in progress, cannot reject")
                if work.workerdone == True:
                    return JsonResponse(
                        {"error": "Work is already done by worker"}, status=400
                    )

                work.delete()
                return JsonResponse({'message': 'Work deleted successfully'})

            if status == 'Done':
                if work.status != 'In Progress':
                    raise ValueError("Work is not in progress, cannot mark as done")

                if(work.workerdone==True):
                    return JsonResponse({'error':"Work is already done by worker"},status=400)

                work.workerdone = True
                work.worker_done_on = timezone.now()

                if work.userdone:
                    work.done_on = timezone.now()
                    work.status = 'Done'

                work.save()

            return JsonResponse({'message': 'Status updated successfully'})

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data in request body'}, status=400)

        except KeyError as e:
            return JsonResponse({'error': str(e)}, status=400)

        except CustomUser.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)

        except CustomWorker.DoesNotExist:
            return JsonResponse({'error': 'Worker not found'}, status=404)

        except WorkHistory.DoesNotExist:
            return JsonResponse({'error': 'Work history not found'}, status=404)

        except ValueError as e:
            return JsonResponse({'error': str(e)}, status=400)

        except Exception as e:
            print(e)
            return JsonResponse({'error': 'Error updating the status'}, status=500)

    else:
        return JsonResponse({"error": "Invalid request method"}, status=400)


@csrf_exempt    
def fetch_timeline_details(request):
    try:
        request_data = json.loads(request.body)
        
        user_email = request_data.get('user_email')
        worker_email = request_data.get('worker_email')
        service = request_data.get('service')
        status = request_data.get('status')
        
        if not all([user_email, worker_email, service]):
            raise KeyError("Missing required fields")

        # Check if the user and worker exist
        user = CustomUser.objects.get(email=user_email)
        worker = CustomWorker.objects.get(email=worker_email)
        
        print(1)
        # Retrieve the work history
        work = WorkHistory.objects.get(user=user, worker=worker, service=service,status=status)
        print(2)

        timeline_data = []
        timeline_data.append({
            'time': work.started_on,
            'title': 'Work Started',                
        })

        if work.user_done_on:

            print(work.user_done_on)
            print('user')
            timeline_data.append(
                {
                    'time': work.user_done_on,                
                    'title': 'User marked the project as Done',                
                }            
            )       

#             timeline_data.append(
#                 {
#                     'time': work.user_done_on,                
#                     'title': f'User gave review {work.user_review} and rating {work.user_rating}',           
#                 }            
#             )


        if work.worker_done_on:
            timeline_data.append({
                'time': work.worker_done_on,
                'title': 'Worker marked the project as Done',                
            })

        if work.done_on:
            timeline_data.append({
                'time': work.done_on,
                'title': 'Work Completed',
            })
        return JsonResponse({'timeline_details': timeline_data})

    except KeyError as e:
        return JsonResponse({'error': str(e)}, status=400)
        
    except CustomUser.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)
    
    except CustomWorker.DoesNotExist:
        return JsonResponse({'error': 'Worker not found'}, status=404)

    except WorkHistory.DoesNotExist:
        return JsonResponse({'error': 'Work history not found'}, status=404)
    
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON format in request body'}, status=400)

    except Exception as e:
        print(e)
        return JsonResponse({'error': 'Error fetching timeline details'}, status=500)

@csrf_exempt
def fetch_reviews(request):
    if request.method == 'POST':
        try:
            request_data = json.loads(request.body)
            user_email = request_data.get('user_email')
            worker_email = request_data.get('worker_email')

            if not all([user_email, worker_email]):
                raise KeyError("Missing required fields")

            # Check if the worker exists
            worker_details = WorkerDetails.objects.get(email=worker_email)
            reviews = worker_details.customer_reviews

            return JsonResponse({'reviews': reviews})

        except KeyError as e:
            return JsonResponse({'error': str(e)}, status=400)

        except WorkerDetails.DoesNotExist:
            return JsonResponse({'error': 'Worker details not found'}, status=404)

        except Exception as e:
            print(e)
            return JsonResponse({'error': 'Error fetching reviews'}, status=500)

    else:
        return JsonResponse({"error": "Invalid request method"}, status=400)
