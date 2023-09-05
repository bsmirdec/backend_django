from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import NotificationOutputSerializer

from .services import create_notification_for_employees, create_notification_for_worksite, delete_notification, notification_is_read
from .selectors import get_notifications_for_user, get_notification


class NotificationsViewListAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        notifications = get_notifications_for_user(user_id=user_id)
        serializer = NotificationOutputSerializer(notifications, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class NotificationIsReadAPI(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        notification = get_notification(pk)
        read_notification = notification_is_read(notification)
        serialized_notification = NotificationOutputSerializer(read_notification).data
        return Response(serialized_notification, status=status.HTTP_200_OK)


class NotificationDeleteAPI(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        notification = get_notification(pk)
        if notification is not None:
            delete_notification(notification)
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"message": "Cette notification n'existe pas"}, status=status.HTTP_404_NOT_FOUND)


class CreateEmployeesNotificationAPI(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        try:
            content = request.data.get("content")
            link = request.data.get("link")
            employees = request.data.get("employees", [])

            if not content or not employees:
                return Response({"message": "Contenu et/ou liste d'utilisateurs manquants."}, status=status.HTTP_400_BAD_REQUEST)

            created_notifications = create_notification_for_employees(employees, content, link)

            if created_notifications:
                return Response({"message": "Notifications créées avec succès."}, status=status.HTTP_201_CREATED)
            else:
                return Response({"message": "Échec de la création des notifications."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except Exception as e:
            return Response({"message": f"Une erreur s'est produite : {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CreateWorksiteNotificationAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            content = request.data.get("content")
            link = request.data.get("link")
            worksite_id = request.data.get("worksite_id")

            if not content or not worksite_id:
                return Response({"message": "Contenu et/ou liste d'utilisateurs manquants."}, status=status.HTTP_400_BAD_REQUEST)

            created_notifications = create_notification_for_worksite(worksite_id, content, link)

            if created_notifications:
                return Response({"message": "Notifications créées avec succès."}, status=status.HTTP_201_CREATED)
            else:
                return Response({"message": "Échec de la création des notifications."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except Exception as e:
            return Response({"message": f"Une erreur s'est produite : {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
