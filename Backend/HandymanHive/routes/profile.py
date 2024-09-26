import base64
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from ..models import (
    AbstractUser,
    CustomUser,
    CustomWorker,
    Service,
    Certification,
    WorkerDetails,
)
import jwt
import json
import cloudinary.uploader
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

UPLOAD_DIR = os.path.join(BASE_DIR, 'certificates')


@csrf_exempt
def get_user_data(request):

    if request.method == "POST":
        try:
            data = json.loads(request.body)
            email = data.get("email")
            isWorker = data.get("isWorker")

            if isWorker == "True":
                user = CustomWorker.objects.get(email=email)
                worker=WorkerDetails.objects.get(email=email)
                
            else:
                user = CustomUser.objects.get(email=email)
            
            profile_pic_url = user.profile_pic.url if user.profile_pic else None

            user_details = {
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
                "phone_number": user.phone_number,
                "age": user.age,
                "gender": user.gender,
                "address": user.address,
                "city": user.city,
                "state": user.state,
                "zip_code": user.zip_code,
                "profile_pic": profile_pic_url,
            }
            if isWorker == "True":
                user_details["verified"] = user.verified
                user_details["rating"]=worker.overall_rating
            else:
                user_details["liveLatitude"] = user.liveLatitude
                user_details["liveLongitude"] = user.liveLongitude
                
            return JsonResponse({"worker_details": user_details})
        except jwt.ExpiredSignatureError:
            return JsonResponse({"error": "Token expired"}, status=300)
        except jwt.InvalidTokenError:
            return JsonResponse({"error": "Invalid token"}, status=300)
        except CustomWorker.DoesNotExist or CustomUser.DoesNotExist:
            return JsonResponse({"error": "User not found"}, status=404)
        except Exception as e:
            print(e)
            return JsonResponse({"error": "Error fetching user data"}, status=500)
    else:
        return JsonResponse({"error": "Invalid request method"}, status=400)

@csrf_exempt
def edit_personal_profile(request):
    if request.method == "POST":
        data = json.loads(request.body)
        try:
            email = data.get("email")
            isWorker = data.get("isWorker")

            if isWorker == "True":
                user = CustomWorker.objects.get(email=email)
            else:
                user = CustomUser.objects.get(email=email)

            user.first_name = data.get("first_name")
            user.last_name = data.get("last_name")
            user.age = data.get("age")
            user.gender = data.get("gender")
            user.address = data.get("address")
            user.city = data.get("city")
            user.state = data.get("state")
            user.zip_code = data.get("zip_code")
            user.phone_number = data.get("phone_number")
            user.save()
            return JsonResponse({"message": "Profile updated successfully"})
        except CustomWorker.DoesNotExist or CustomUser.DoesNotExist:
            return JsonResponse({"error": "Email does not exist."}, status=404)
        except Exception as e:
            return JsonResponse({"error": "Error updating profile"}, status=500)

@csrf_exempt
def upload_profile_pic(request):
    if request.method == "POST":
        try:
            print(1)
            data = json.loads(request.body)
            image_file = data.get("image")
            image_data = base64.b64decode(image_file)  # Decoding base64 data
            email = data.get("email")
            isWorker = data.get("isWorker")
            print(email)
            print(isWorker)
            print(image_file)
            if isWorker == "True":
                user = CustomWorker.objects.get(email=email)
            else:
                user = CustomUser.objects.get(email=email)
            print(3)
            upload_result = cloudinary.uploader.upload(image_data)
            print(4)
            image_url = upload_result.get("secure_url")
            print(2)
            user.profile_pic = image_url
            user.save()
            return JsonResponse({"message": "Image uploaded successfully","url":image_url})
        except CustomUser.DoesNotExist:
            return JsonResponse({"error": "User not found"}, status=404)
        except Exception as e:
            return JsonResponse(
                {"error": "Error uploading image: {}".format(str(e))}, status=500
            )
    else:
        return JsonResponse({"error": "Invalid request method"}, status=400)

@csrf_exempt
def update_worker_location(request):
    if request.method == "POST":
        data = json.loads(request.body)
        try:
            email = data.get("email")
            live_latitude = data.get("liveLatitude")
            live_longitude = data.get("liveLongitude")

            worker = WorkerDetails.objects.get(email=email)

            worker.liveLatitude = live_latitude
            worker.liveLongitude = live_longitude
            worker.save()

            return JsonResponse({"message": "Worker location updated successfully"})
        except WorkerDetails.DoesNotExist:
            return JsonResponse({"error": "Worker not found"}, status=404)
        except Exception as e:
            print(e)
            return JsonResponse({"error": "Error updating worker location"}, status=500)
    else:
        return JsonResponse({"error": "Invalid request method"}, status=400)

@csrf_exempt
def update_user_location(request):
    if request.method == "POST":
        data = json.loads(request.body)
        try:
            email = data.get("email")
            live_latitude = data.get("liveLatitude")
            live_longitude = data.get("liveLongitude")

            user = CustomUser.objects.get(email=email)

            user.liveLatitude = live_latitude
            user.liveLongitude = live_longitude
            user.save()

            return JsonResponse({"message": "User location updated successfully"})
        except WorkerDetails.DoesNotExist:
            return JsonResponse({"error": "User not found"}, status=404)
        except Exception as e:
            print(e)
            return JsonResponse({"error": "Error updating user location"}, status=500)
    else:
        return JsonResponse({"error": "Invalid request method"}, status=400)


@csrf_exempt
def delete_user(request):
    if request.method == "POST":
        data = json.loads(request.body)
        email = data.get("email")
        isWorker = data.get("isWorker")

        if isWorker == "True" and CustomWorker.objects.filter(email=email).exists():
            user = CustomWorker.objects.get(email=email)
            user.delete()

        if isWorker == "False" and CustomUser.objects.filter(email=email).exists():
            user = CustomUser.objects.get(email=email)
            user.delete()

        if AbstractUser.objects.filter(email=email).exists():
            user = AbstractUser.objects.get(email=email)
            user.delete()

        return JsonResponse({"message": "User deleted successfully"})

    return JsonResponse({"error": "Invalid request method"}, status=400)


# -----------------WORKER PROFESSIONAL PROFILE ------------------------

######################## SERVICES #############################

@csrf_exempt
def update_services(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            email = data.get("email")
            services = data.get("services")
            print("services=",services)
            print("email=",email)
            # print(1)
            worker = WorkerDetails.objects.get(email=email)
            worker.services_offered.clear()
            # print(2)
            for service in services:
                try:
                    obj, is_created = Service.objects.get_or_create(name=service)
                    worker.services_offered.add(obj)                  
                except Exception as e:
                    print(e)
                    return JsonResponse({"error": "Error updating services"}, status=500)
                    
                    

            return JsonResponse({"message": "Services updated successfully"})

        except Exception as e:
            return JsonResponse({"error": "Error updating services"}, status=500)

    else:
        return JsonResponse({"error": "Invalid request method"}, status=400)


@csrf_exempt
def get_services(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            email = data.get("email")
            worker = WorkerDetails.objects.get(email=email)

            services = worker.services_offered.all()
            

            worker_services = []

            for service in services:
                worker_services.append({"name": service.name})

        except Exception as e:
            return JsonResponse({"error": "Error fetching services"}, status=500)

    else:
        return JsonResponse({"error": "Invalid request method"}, status=400)

@csrf_exempt
def get_workers(request):
    if request.method == "GET":
        try:
            # Query all worker profiles
            workers = CustomWorker.objects.all()

            # Initialize an empty list to store worker data
            workers_data = []

            # Extract required information for each worker
            for worker in workers:
                worker_data = {
                    "name": f"{worker.first_name} {worker.last_name}",
                    "email": worker.email,
                    "verified": worker.verified
                }
                workers_data.append(worker_data)

            # Create JSON response
            return JsonResponse({"workers": workers_data})

        except Exception as e:
            return JsonResponse({"error": "Error fetching workers"}, status=500)

    else:
        return JsonResponse({"error": "Invalid request method"}, status=400)


######################## WORKER CERTIFICATIONS #########################

@csrf_exempt
def upload_certificate(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            email = data.get('email')
            certificate_name = data.get('certificate_name')
            certificate_data = data.get('certificate')            
            
            if not os.path.exists(UPLOAD_DIR):
                os.makedirs(UPLOAD_DIR)
            
            pdf_filename = email + "#" + certificate_name + ".pdf"    
            pdf_file_path = os.path.join(UPLOAD_DIR, pdf_filename)
            certificate_bytes = base64.b64decode(certificate_data)
            
            with open(pdf_file_path, 'wb') as f:
                f.write(certificate_bytes)
            
                          
            if Certification.objects.filter(certificate_name=certificate_name, worker_email=email).exists():
                return JsonResponse({"error": "Certificate already uploaded"}, status=400)
                      
            certificate = Certification.objects.create(
                certificate_name=certificate_name,
                worker_email=email,
                certificate_data=pdf_filename                
            ) 
            
            return JsonResponse({"message": "Certificate uploaded successfully"})       
            
            

        except Exception as e:
            print(e)
            return JsonResponse({"error": "Error uploading certificate"}, status=500)

    else:
        return JsonResponse({"error": "Invalid request method"}, status=400)


@csrf_exempt
def get_certificates(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            email = data.get("email")

            certificates = Certification.objects.filter(worker_email=email)
            worker_details= WorkerDetails.objects.get(email=email)

            certificate_data = []
            for certificate in certificates:
                pdf_filename = certificate.certificate_data    
                pdf_file_path = os.path.join(UPLOAD_DIR, pdf_filename)

                if os.path.exists(pdf_file_path):
                    with open(pdf_file_path, 'rb') as f:
                        pdf_content_bytes = f.read()
                        pdf_content_base64 = base64.b64encode(pdf_content_bytes).decode('utf-8')

                    certificate_data.append(
                        {
                            "certificate_name": certificate.certificate_name,
                            "issuing_authority": certificate.issuing_authority,
                            "certificate_data": pdf_content_base64,
                            "added_on": certificate.created_on,
                            "status": certificate.status,
                        }
                    )

            return JsonResponse(
                {
                    "certificates": certificate_data,
                    "rating": worker_details.overall_rating,
                }
            )
        except Exception as e:
            print(e)
            return JsonResponse({"error": "Error fetching certificates"}, status=500)
    else:
        return JsonResponse({"error": "Invalid request method"}, status=400)

@csrf_exempt
def approve_certificate(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            worker_email = data.get("worker_email")
            certificate_name = data.get("certificate_name")

            certificate = Certification.objects.get(
                worker_email=worker_email, certificate_name=certificate_name
            )

            certificate.status = "Approved"
            certificate.save()

            return JsonResponse({"message": "Certificate approved successfully"})
        except Certification.DoesNotExist:
            return JsonResponse({"error": "Certificate not found"}, status=404)
        except Exception as e:
            return JsonResponse({"error": "Error approving certificate"}, status=500)
    else:
        return JsonResponse({"error": "Invalid request method"}, status=400)


@csrf_exempt
def worker_verification_status(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            email = data.get("email")

            certificates = Certification.objects.filter(worker_email=email)

            total_certificates = 0
            verified_certificates = 0

            for certificate in certificates:
                total_certificates += 1
                if certificate.status == "approved":
                    verified_certificates += 1

            if total_certificates > 0:
                verification_ratio = verified_certificates / total_certificates
            else:
                verification_ratio = 0

            return JsonResponse({"verification_ratio": verification_ratio})
        except Exception as e:
            return JsonResponse({"error": "Error fetching certificates"}, status=500)
    else:
        return JsonResponse({"error": "Invalid request method"}, status=400)
