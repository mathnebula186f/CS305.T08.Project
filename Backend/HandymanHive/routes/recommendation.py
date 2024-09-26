from django.db.models import F
from django.db.models import ExpressionWrapper, FloatField
from django.db.models.functions import ACos, Cos, Radians, Sin, Sqrt
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import F
from ..models import (
    CustomWorker,
    Service,
    WorkerDetails,
    WorkHistory
)
import json



@csrf_exempt
def get_workers_on_price(request):
    if request.method == "GET":
        
        try:
            service_name = request.GET.get('service_name')
            service = Service.objects.get(name=service_name)
            top_five_workers_details = (
                WorkerDetails.objects.filter(isAvailable=True)
                .filter(services_offered__in=[service])
                .annotate(average_price=(F("min_price") + F("max_price")) / 2)
                .order_by("average_price")[:5]
            )

            top_five_workers = []
            for worker_detail in top_five_workers_details:
                worker = CustomWorker.objects.get(email=worker_detail.email)
                worker_data = {
                    "email": worker.email,
                    "first_name": worker.first_name,
                    "last_name": worker.last_name,
                }
                top_five_workers.append(worker_data)

            return JsonResponse({"top_five_custom_workers": top_five_workers})
        except Service.DoesNotExist:
            return JsonResponse({"error": "Service not found"}, status=404)
        except WorkerDetails.DoesNotExist:
            return JsonResponse({"error": "WorkerDetails not found"}, status=404)
        except Exception as e:
            print(e)
            return JsonResponse({"error": "Error fetching worker data"}, status=500)
    else:
        return JsonResponse({"error": "Invalid request method"}, status=400)


@csrf_exempt
def get_nearest_workers(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            service_name = data.get("service")
            user_coords = data.get("coords")
            print("coords=", user_coords)
            print("Given service_name=", service_name)

            user_latitude_rad = Radians(user_coords[0])
            user_longitude_rad = Radians(user_coords[1])
            all_services = Service.objects.all()

            # Iterate over each service and print its details
            # print("lentgh=",len(all_services))
            # for service in all_services:
            #     print(f"Service Name: {service.name}")
            # # print("Here are the services=",Service.objects.all())
            service = Service.objects.get(name=service_name)

            # print("Here")
            workers = (
                WorkerDetails.objects.filter(services_offered__in=[service])
                .annotate(
                    latitude_radians=ExpressionWrapper(
                        Radians(F("liveLatitude")), output_field=FloatField()
                    ),
                    longitude_radians=ExpressionWrapper(
                        Radians(F("liveLongitude")), output_field=FloatField()
                    ),
                    dlat=ExpressionWrapper(
                        Sin((F("latitude_radians") - user_latitude_rad) / 2) ** 2,
                        output_field=FloatField(),
                    ),
                    dlon=ExpressionWrapper(
                        Sin((F("longitude_radians") - user_longitude_rad) / 2) ** 2,
                        output_field=FloatField(),
                    ),
                    a=ExpressionWrapper(
                        (
                            F("dlat")
                            + Cos(user_latitude_rad)
                            * Cos(F("latitude_radians"))
                            * F("dlon")
                        ),
                        output_field=FloatField(),
                    ),
                    c=ExpressionWrapper(
                        2 * ACos(Sqrt(F("a"))), output_field=FloatField()
                    ),
                    distance=ExpressionWrapper(
                        6371 * F("c"), output_field=FloatField()
                    ),
                )
                .order_by("distance")[:5]
            )
            print(1)

            worker_details = []

            for worker in workers:
                print(worker.email)
                details = CustomWorker.objects.get(email=worker.email)
                details2=WorkerDetails.objects.get(email=worker.email)
                worker_details.append(
                    {
                        "first_name": details.first_name,
                        "last_name": details.last_name,
                        "email": details.email,
                        "liveLatitude": worker.liveLatitude,
                        "liveLongitude": worker.liveLongitude,
                        "rating": details2.overall_rating,
                    }
                )
            print("Worker Details", worker_details)

            return JsonResponse({"workers": worker_details})

        except Exception as e:
            print(e)
            return JsonResponse({"error": "Error fetching workers"}, status=500)
    else:
        return JsonResponse({"error": "Invalid request method"}, status=400)
    
    
@csrf_exempt    
def get_all_services(request):
    if request.method=='POST':
        try:
            data = json.loads(request.body)            
            services = Service.objects.all()
            service_list = []
            for service in services:
                service_list.append({
                    "name":service.name,
                    "description":service.description
                    }
                )
                
            services                 
            return JsonResponse({"services":service_list})
        
        except Exception as e:
            print(e)
            return JsonResponse({"error":"Error fetching services"}, status=500)

    else:
        return JsonResponse({"error": "Invalid request method"}, status=400)

@csrf_exempt    
def get_top_trending_services(request):
    if request.method=='POST':
        try:
            data = json.loads(request.body)            
            services = Service.objects.all()
            service_dict = {}
            for service in services:
                service_dict[service.name]=0
            
            works= WorkHistory.objects.all() 
            for work in works:
               if Service.objects.filter(name=work.service):
                   service_dict[work.service]+=1
            
            services = sorted(service_dict.items(), key=lambda item: item[1], reverse=True)[:10]  
             
            service_list = [{"name":service[0], "count": service[1]} for service in services]
                            
            return JsonResponse({"top_services":service_list})        
        except Exception as e:
            print(e)
            return JsonResponse({"error":"Error fetching services"}, status=500)
        
    else:
        return JsonResponse({"error": "Invalid request method"}, status=400)