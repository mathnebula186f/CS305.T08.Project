import json
from django.http import JsonResponse
import requests


templates = {
    "Accepted Work": {
        "title": "{service} Request Accepted",
        "body": "Your {service} request has been accepted by {user}."
    },
    "Request Work": {
        "title": "New {service} Request",
        "body": "You have a new request by {user}!"
    },
    "Work Completed": {
        "title": "Work Completed",
        "body": "Your work request has been completed."
    },
    "Work Cancelled": {
        "title": "Work Cancelled",
        "body": "Your work request has been cancelled."
    },
    "Thanks":{
        "title": "Thanks for using Handyman Hive",
        "body": "Thank you for using Handyman Hive. We hope you had a great experience."
    },
}

def send_notfication(template, user, data=None):
    try:
        title= templates[template]['title'].format(**data) if data and 'service' in data and 'user' in data else templates[template]['title']
        body= templates[template]['body'].format(**data) if data and 'service' in data and 'user' in data else templates[template]['body']
        print(title, body)
        resp=requests.post("https://exp.host/--/api/v2/push/send", 
            headers={
                'Accept': 'application/json',
                'Accept-Encoding': 'gzip, deflate',
                'Content-Type': 'application/json'
            },
            data=json.dumps({
                'to': user.get_notification_tokens()[0],
                'sound': 'default',
                'title': templates[template]['title'].format(**data) if data and 'service' in data and 'user' in data else templates[template]['title'],
                'body': templates[template]['body'].format(**data) if data and 'service' in data and 'user' in data else templates[template]['body'],
            })
            )
        print(resp)
        return "Success"
    except Exception as e:
        print(e)
        return "Failed"