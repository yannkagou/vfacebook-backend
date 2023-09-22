from django.http import JsonResponse
from rest_framework.decorators import api_view
from .models import Notification
from .serialiazers import NotificationSerializer

@api_view(['GET'])
def notifications(request):
    received_notifications = request.user.received_notifications.filter(is_read=False)
    serializer = NotificationSerializer(received_notifications, many=True)
    
    return JsonResponse(serializer.data, safe=False)

@api_view(['GET'])
def allnotifications(request):
    received_notifications = request.user.received_notifications
    serializer = NotificationSerializer(received_notifications, many=True)
    
    return JsonResponse(serializer.data, safe=False)

@api_view(['POST'])
def read_notification(request, id):
    notification = Notification.objects.filter(created_for=request.user).get(id=id)
    notification.is_read = True
    notification.save()
    
    return JsonResponse({'message': 'notification read'})



# from django.http import JsonResponse
# from rest_framework.decorators import api_view
# from .models import Notification
# from .serialiazers import NotificationSerializer

# @api_view(['GET'])
# def notifications(request):
#     received_notifications = request.user.received_notifications
#     serializer = NotificationSerializer(received_notifications, many=True)
    
#     return JsonResponse(serializer.data, safe=False)

# @api_view(['POST'])
# def read_notification(request, id):
#     notification = Notification.objects.filter(created_for=request.user).get(id=id)
#     notification.is_read = True
#     notification.save()
    
#     return JsonResponse({'message': 'notification read'})