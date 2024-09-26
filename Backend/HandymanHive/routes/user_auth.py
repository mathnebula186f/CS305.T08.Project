from datetime import timedelta
import os
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.conf import settings
from django.db.models import F
from ..models import (
    AbstractUser,
    CustomUser,
    CustomWorker,
    WorkerDetails,
)
import jwt
import json
import random
import string
from django.core.mail import send_mail

adminlist = [
    "2021csb1062@iitrpr.ac.in",
    "2021csb1124@iitrpr.ac.in",
    "alankritkadian@gmail.com",
    "2021csb1090@iitrpr.ac.in",
    # "mani15102002@gmail.com",
]


def generate_otp(length=6):
    characters = string.digits
    otp = "".join(random.choice(characters) for _ in range(length))
    print("otp: ",otp)
    return otp


def send_otp_email(email, otp, type="Login"):
    subject = "Your OTP for {type}"
    message = f"Your OTP is: {otp}"
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, from_email, recipient_list)



@csrf_exempt
def user_signup(request):
    if request.method == "POST":
        data = json.loads(request.body)
        email = data.get("email")
        isWorker = data.get("isWorker")
        print("Value of isWorker in user_signup is =", isWorker)

        if isWorker == "True" and CustomWorker.objects.filter(email=email).exists():
            return JsonResponse({"error": "Email already exists"}, status=405)

        if isWorker == "False" and CustomUser.objects.filter(email=email).exists():
            return JsonResponse({"error": "Email already exists"}, status=405)
        print("I have passed if ")

        if AbstractUser.objects.filter(email=email).exists():
            try:
                user = AbstractUser.objects.get(email=email)
                otp = generate_otp()
                # print("Generated Otp=",otp)
                user.otp = otp
                user.otp_valid_till = timezone.now() + timedelta(minutes=15)
                user.user_details = json.dumps(data)
                user.is_worker = isWorker
                user.save()

                # Send OTP to user
                send_otp_email(email, otp, "Signup")
                return JsonResponse({"message": "OTP sent successfully"})
            except Exception as e:
                print(e)
                return JsonResponse({"error": "Error sending OTP"}, status=500)

        try:
            user = AbstractUser.objects.create(
                email=email,
                otp_valid_till=timezone.now() + timedelta(minutes=15),
                user_details=json.dumps(data),
                is_worker=isWorker,
            )
            otp = generate_otp()
            user.otp = otp
            user.save()
            send_otp_email(email, otp)
            return JsonResponse({"message": "OTP sent successfully"})
        except Exception as e:
            print(e)
            return JsonResponse({"error": "Error sending OTP"}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=400)


@csrf_exempt
def verify_otp(request):
    if request.method == "POST":
        data = json.loads(request.body)
        email = data.get("email")
        otp = data.get("otp")
        isWorker = data.get("isWorker")
        notification_id=data.get("notification_id")
        if isWorker == "True" and CustomWorker.objects.filter(email=email).exists():
            return JsonResponse({"error": "Email already exists"}, status=405)

        if isWorker == "False" and CustomUser.objects.filter(email=email).exists():
            return JsonResponse({"error": "Email already exists"}, status=405)
        print(1)
        try:
            user = AbstractUser.objects.get(email=email)
            if str(user.is_worker) != isWorker:
                return JsonResponse({"message": "User not found"}, status=404)

            print(str(user.is_worker), isWorker, 2)
            if user.otp == otp and user.otp_valid_till > timezone.now():
                user_data = json.loads(user.user_details)

                if isWorker == "True":
                    user = CustomWorker.objects.create(
                        phone_number=user_data["phone_number"],
                        first_name=user_data["first_name"],
                        last_name=user_data["last_name"],
                        email=user_data["email"],
                        age=int(user_data["age"] or 0),
                        gender=user_data["gender"],
                        address=user_data["address"],
                        city=user_data["city"],
                        state=user_data["state"],
                        zip_code=user_data["zip_code"],
                        # notification_token=notification_id
                    )
                    user.add_notification_token(notification_id)
                    worker_details = WorkerDetails.objects.create(
                        email=user_data["email"]
                    )
                    worker_details.save()
                    user.save()
                else:
                    user = CustomUser.objects.create(
                        phone_number=user_data["phone_number"],
                        first_name=user_data["first_name"],
                        last_name=user_data["last_name"],
                        email=user_data["email"],
                        age=int(user_data["age"]),
                        gender=user_data["gender"],
                        address=user_data["address"],
                        city=user_data["city"],
                        state=user_data["state"],
                        zip_code=user_data["zip_code"],
                        # notification_token=notification_id
                    )
                    user.add_notification_token(notification_id)
                    user.save()

                payload = {
                    "email": user.email,
                    "exp": timezone.now() + timedelta(days=1),
                    "iat": timezone.now(),
                }

                isAdmin = False
                for em in adminlist:
                    if em == email:
                        isAdmin = True
                if isAdmin:
                    response = JsonResponse(
                        {"message": "OTP verified successfully", "isAdmin": "True"}
                    )
                else:
                    response = JsonResponse(
                        {"message": "OTP verified successfully", "isAdmin": "False"}
                    )
                token = jwt.encode(payload, os.getenv("Secret_Key"), algorithm="HS256")

                response.set_cookie(
                    "token", token, expires=payload["exp"], secure=True, httponly=True
                )
                return response

            elif user.otp_valid_till < timezone.now():
                return JsonResponse({"error": "OTP expired"}, status=300)
            else:
                return JsonResponse({"error": "Invalid OTP"}, status=300)
        except Exception as e:
            print(e)
            return JsonResponse({"error": "Error Verifying OTP"}, status=500)
    else:
        return JsonResponse({"error": "Invalid request method"}, status=400)


@csrf_exempt
def user_login(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            email = data.get("email")
            isWorker = data.get("isWorker")

            print("Value of isWorker in userLogin=", isWorker)

            if isWorker == "True":
                user_model = CustomWorker
                # user = CustomWorker.objects.get(email=email)
            else:
                user_model = CustomUser
                # user = CustomUser.objects.get(email=email)

            try:
                user = user_model.objects.get(email=email)
            except user_model.DoesNotExist:
                return JsonResponse(
                    {"error": "User with this email does not exist."}, status=404
                )
            # print("im Here")
            otp = generate_otp()
            # print("Generatd Otp=",otp)
            user.otp = otp
            user.otp_valid_till = timezone.now() + timedelta(minutes=50)
            user.save()

            send_otp_email(email, otp)

            return JsonResponse({"message": "OTP sent successfully"})
        except Exception as e:
            print(e)
            return JsonResponse({"error": "Error sending OTP"}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=400)


@csrf_exempt
def verify_login_otp(request):
    if request.method == "POST":
        data = json.loads(request.body)
        email = data.get("email")
        otp = data.get("otp")
        isWorker = data.get("isWorker")
        notification_id = data.get("notification_id")
        print("isWorker=", isWorker)

        try:
            if isWorker == "True":
                user = CustomWorker.objects.get(email=email)
            else:
                user = CustomUser.objects.get(email=email)

            print("userotp=", user.otp)
            print("otp=", otp)
            user.add_notification_token(notification_id)
            if str(user.otp) == str(otp) and user.otp_valid_till > timezone.now():
                user.add_notification_token(notification_id)

                payload = {
                    "email": user.email,
                    "exp": timezone.now() + timedelta(days=1),
                    "iat": timezone.now(),
                }
                print("otp=", otp)
                token = jwt.encode(payload, os.getenv("Secret_Key"), algorithm="HS256")
                print("token during login=", token)

                # response.set_cookie(
                #     "token", token, expires=None, secure=True, samesite='None'
                # )
                isAdmin = False
                for em in adminlist:
                    if em == email:
                        isAdmin = True
                if isAdmin:
                    response = JsonResponse(
                        {
                            "message": "OTP verified successfully",
                            "isAdmin": "True",
                            "token": token,
                        }
                    )
                else:
                    response = JsonResponse(
                        {
                            "message": "OTP verified successfully",
                            "isAdmin": "False",
                            "token": token,
                        }
                    )

                return response

            elif user.otp_valid_till < timezone.now():
                return JsonResponse({"error": "OTP expired"}, status=500)
            else:
                return JsonResponse({"error": "Invalid OTP"})
        except CustomWorker.DoesNotExist or CustomUser.DoesNotExist:
            return JsonResponse(
                {"error": "User with this email does not exist."}, status=404
            )
        except Exception as e:
            print(e)
            return JsonResponse({"error": "Invalid OTP"}, status = 404)
    else:
        return JsonResponse({"error": "Invalid request method"})
