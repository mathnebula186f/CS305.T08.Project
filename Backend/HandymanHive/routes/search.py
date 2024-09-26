from django.db.models import Q
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from ..models import (
    CustomUser,
    CustomWorker,
    Service,
    WorkerDetails,
)
import json
import random
import string
from .hfcb import HuggingChat as HCA
import os
from datetime import timedelta
from django.utils import timezone



############################ SEARCH FUNCTIONALITY ########################


@csrf_exempt
def get_closest_services(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            query = data.get("query")
            email = data.get("email")
            user = CustomUser.objects.get(email=email)
            
            # Add the query using the add_query method
            user.add_query(query)
            user.save()           
            
            
            
            service_objects = Service.objects.all()
            services = [service.name for service in service_objects]

            prompt = f"""Given a list of home utility services {services} and an input query by the homeowner: 
            "{query}", 
            identify the services needed by the homeowner to resolve the query.

            Return a JSON object of up to 3 services needed by the homeowner to resolve the query in decreasing order of relevance to the query. 
            If fewer than 3 services have decent relevance, return only relevant services. The list may be empty if no service has good enough relevance with the query.
            """
            prompt+= '''
            Format of Output: 
            {'services': ['service1', 'service2', 'service3']}
            
            For example:
            Services: [plumbing, electrical repair, HVAC maintenance, appliance repair, carpentry, gardening, cleaning]
            Query: "My kitchen sink is leaking and needs immediate fixing."
            Output: {'services': ['plumbing', 'appliance repair']}                     
            
            '''
            # llm = HCA(email=os.getenv("HF_EMAIL"), psw=os.getenv("HF_PASSWORD"), cookie_path="./cookies_snapshot")
            # response = llm(prompt)   
            
            query_list = query.split(' ')
            query_list = [word.lower() for word in query_list]
            response=''
            if any(term in query_list for term in ["hair", "salon", "barber", "haircut", "hairdresser", "hairstyle"]):
                response = "['Barber', 'Salon', 'Hair Care', 'Beauty Services']"
            if any(term in query_list for term in ["plumbing", "leak", "pipes", "faucet", "sink", "pipe"]):
                response = "['Plumbing', 'Home Repair', 'Maintenance Services']"
            if any(term in query_list for term in ["bulb", "light", "switch", "electric", "power", "socket"]):
                response = "['Electrical', 'Appliance Repair', 'HVAC']"
            if any(term in query_list for term in ["carpentry", "wood", "furniture"]):
                response = "['Carpentry', 'Furniture Assembly', 'Home Renovation']"
            if any(term in query_list for term in ["painting", "color", "wall"]):
                response = "['Painting', 'Interior Design', 'Exterior Painting', 'Wallpaper Removal']"
            if any(term in query_list for term in ["landscaping", "garden", "plant", "lawn"]):
                response = "['Landscaping', 'Gardening', 'Tree Trimming', 'Deck Construction']"
            if any(term in query_list for term in ["roof", "leak", "shingles"]):
                response = "['Roofing', 'Water Damage Restoration', 'Home Renovation', 'Foundation Repair']"
            if any(term in query_list for term in ["floor", "tile", "carpet", "hardwood"]):
                response = "['Flooring', 'Carpet Cleaning', 'Home Renovation', 'Basement Waterproofing']"
            if any(term in query_list for term in ["heat", "cold", "temperature", "HVAC"]):
                response = "['HVAC (Heating, Ventilation, and Air Conditioning)', 'Home Insulation', 'Home Automation', 'Solar Panel Installation']"
            if any(term in query_list for term in ["appliance", "fridge", "oven", "washer"]):
                response = "['Appliance Repair', 'Home Renovation', 'Kitchen Remodeling']"
            if any(term in query_list for term in ["window", "glass", "curtain", "blinds"]):
                response = "['Window Cleaning', 'Interior Design', 'Home Cleaning', 'Home Renovation']"
            if any(term in query_list for term in ["pressure", "wash", "clean", "dirt"]):
                response = "['Pressure Washing', 'Home Cleaning', 'Carpet Cleaning', 'Deck Construction']"
            if any(term in query_list for term in ["pest", "bug", "insect", "rodent"]):
                response = "['Pest Control', 'Home Cleaning']"    
             
            if response =='':
               response = "['Home Clean', 'Carpentry', 'Barber', 'Salon', 'Painter']"
            
                     
            response = response.split("[")[1].split("]")[0]
            response = '[' + response + ']'
            response_json = response.replace("'", "\"")
            services = json.loads(response_json)
            print(response)
            
            closest_workers = []
            workers = CustomWorker.objects.filter(
                Q(first_name__icontains=query) | Q(last_name__icontains=query)
            )[:5]

            for worker in workers:
                closest_workers.append(
                    {
                        "first_name": worker.first_name,
                        "last_name": worker.last_name,
                        "email": worker.email,
                    }
                )
            print("Here are the services=",services)
            return JsonResponse({"services": services, "workers": closest_workers}) 

        except Exception as e:
            print(e)
            return JsonResponse({"error": "Error fetching service"}, status=500)
    else:
        return JsonResponse({"error": "Invalid request method"}, status=400)

@csrf_exempt
def user_last_five_queries(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            email = data.get("email")
            user = CustomUser.objects.get(email=email)
            last_five_queries = user.get_last_five_queries()
            return JsonResponse({"last_five_queries": last_five_queries})
        except CustomUser.DoesNotExist:
            return JsonResponse({"error": "Email does not exist"}, status=404)
    else:
        return JsonResponse({"error": "Invalid Request Method"}, status=400)


################################## HELPER FUNCTIONS ####################################
@csrf_exempt
def insert_worker(request):
    try:
        SERVICES = [
            "Plumbing",
            "Electrical",
            "Carpentry",
            "Painting",
            "Landscaping",
            "Gardening",
            "Roofing",
            "Flooring",
            "HVAC (Heating, Ventilation, and Air Conditioning)",
            "Appliance Repair",
            "Window Cleaning",
            "Pressure Washing",
            "Pest Control",
            "Home Security Installation",
            "Drywall Repair",
            "Furniture Assembly",
            "Interior Design",
            "Home Cleaning",
            "Carpet Cleaning",
            "Masonry",
            "Fence Installation",
            "Deck Construction",
            "Gutter Cleaning",
            "Tree Trimming",
            "Pool Maintenance",
            "Locksmith",
            "Garage Door Repair",
            "Water Damage Restoration",
            "Kitchen Remodeling",
            "Bathroom Remodeling",
            "Home Theater Installation",
            "Home Automation",
            "Solar Panel Installation",
            "Septic Tank Services",
            "Exterior Painting",
            "Siding Installation",
            "Wallpaper Removal",
            "Home Insulation",
            "Chimney Cleaning",
            "Foundation Repair",
            "Basement Waterproofing",
            "Drain Cleaning",
            "Welding Services",
            "Elevator Installation",
            "Bathtub Refinishing",
            "Countertop Installation",
            "Ceiling Fan Installation",
            "Fireplace Installation",
            "Shower Installation",
            "Security Camera Installation",
            "Ceiling Repair",
            "Home Renovation",
            "Shed Construction",
        ]
        FIRST = [
            "James",
            "John",
            "Robert",
            "Michael",
            "William",
            "David",
            "Richard",
            "Joseph",
            "Charles",
            "Thomas",
            "Mary",
            "Jennifer",
            "Linda",
            "Patricia",
            "Elizabeth",
            "Barbara",
            "Susan",
            "Jessica",
            "Sarah",
            "Karen",
            "Daniel",
            "Matthew",
            "Anthony",
        ]

        LAST = [
            "Smith",
            "Johnson",
            "Williams",
            "Jones",
            "Brown",
            "Davis",
            "Miller",
            "Wilson",
            "Moore",
            "Taylor",
            "Anderson",
            "Thomas",
            "Jackson",
            "White",
            "Harris",
            "Martin",
            "Thompson",
            "Garcia",
            "Martinez",
            "Robinson",
            "Clark",
            "Rodriguez",
            "Lewis",
            "Lee",
        ]
        for i in FIRST:
            for j in LAST:

                try:
                    phone_number = "".join(random.choices(string.digits, k=10))
                    first_name = i
                    last_name = j
                    email = f"{first_name.lower()}.{last_name.lower()}@gmail.com"
                    age = "25"
                    gender = "Male"
                    address = "address"
                    city = "city"
                    state = "city"
                    zip_code = "zip_code"
                    num_services = random.randint(1, len(SERVICES))
                    services = random.sample(SERVICES, num_services)
                    latitude = round(random.uniform(30.8, 31.2), 4)
                    longitude = round(random.uniform(76.4, 76.8), 4)


                    if CustomWorker.objects.filter(email=email).exists():
                        worker = CustomWorker.objects.get(email=email)  
                    else:
                        worker = CustomWorker.objects.get_or_create(
                            phone_number=phone_number,
                            first_name=first_name,
                            last_name=last_name,
                            email=email,
                            age=age,
                            gender=gender,
                            address=address,
                            city=city,
                            state=state,
                            zip_code=zip_code,
                            otp="1234",
                            otp_valid_till=timezone.now() + timedelta(days=30),
                        )
        
                    try: 
                        worker_details = WorkerDetails.objects.create(
                            email=email,
                            liveLatitude=latitude,
                            liveLongitude=longitude                                
                        )
                    except:
                        worker_details=WorkerDetails.objects.get(email=email)
                        
        
                    for serv in SERVICES:
                        # print(serv)
                        if Service.objects.filter(name=serv).exists():
                            # print(1)
                            service = Service.objects.get(name=serv)
                        else:
                            # print(2)
                            service = Service.objects.create(name=serv)

                                           
                            
                        
                        worker_details.services_offered.add(service)
                

                    worker_details.save()
                    worker.save()
                except Exception as e:
                    print(e)
                    pass
        return JsonResponse({"message": "Worker added successfully"})

    except Exception as e:
        print(e)
        return JsonResponse({"error": "Error adding worker"}, status=500)
