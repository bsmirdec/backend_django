import json
import datetime
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from ..permissions.CRUDpermissions import CustomPermissionMixin
from .serializers import DeliveryInputSerializer, DeliveryOutputSerializer, DeliveryLineOutputSerializer
from .services import delivery_create, delivery_lines_create, delivery_update, delivery_confirm, delivery_delete, delivery_lines_delete
from .selectors import deliveries_get_list, delivery_get_object, delivery_lines_get_list


class DeliveryViewListAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, employee_id):
        deliveries = deliveries_get_list(employee_id)
        if deliveries:
            serializer = DeliveryOutputSerializer(deliveries, many=True)
            return Response(serializer.data)
        else:
            return Response({"message": "Pas de livraisons programmées"}, status=status.HTTP_404_NOT_FOUND)


class DeliveryRetrieveObjectAPI(CustomPermissionMixin, APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, delivery_id):
        delivery = delivery_get_object(delivery_id)
        if delivery:
            response_data = DeliveryOutputSerializer(delivery).data
            return Response(response_data)
        else:
            return Response("Erreur dans la récupération de la livraison", status=status.HTTP_404_NOT_FOUND)


class DeliveryLinesViewListAPI(CustomPermissionMixin, APIView):
    def get(self, request, delivery_id):
        delivery_lines = delivery_lines_get_list(delivery_id)
        serializer = DeliveryLineOutputSerializer(delivery_lines, many=True)
        return Response(serializer.data)


class DeliveryCreateObjectAPI(CustomPermissionMixin, APIView):
    def post(self, request):
        if self.has_permission(request, self):
            delivery_data = request.data.get("order")
            delivery_lines_data = request.data.get("order_lines")
            delivery_lines_data = json.loads(delivery_lines_data)

            # Création de la commande
            delivery_serializer = DeliveryInputSerializer(data=delivery_data)
            if delivery_serializer.is_valid():
                delivery_instance = delivery_create(delivery_serializer.validated_data)
                delivery_data = DeliveryOutputSerializer(delivery_instance).data

                # Création des lignes de commandes associées
                delivery_lines_data = delivery_lines_create(delivery_lines_data, delivery_id=delivery_instance.order_id)
                if delivery_lines_data:
                    response_dict = {
                        "delivery_data": delivery_data,
                        "delivery_lines": delivery_lines_data,
                    }
                    return Response(response_dict, status=status.HTTP_201_CREATED)
                else:
                    return Response("Erreur avec l'enregistrement des produits", status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(delivery_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("Permission denied", status=status.HTTP_403_FORBIDDEN)


class DeliveryUpdateObjectAPI(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, delivery_id):
        delivery = delivery_get_object(delivery_id)
        delivery_data = request.data.get("delivery")
        delivery_data["order"] = delivery_data["order"]["order_id"]
        delivery_data["worksite"] = delivery_data["worksite"]["worksite_id"]
        if delivery:
            serializer = DeliveryInputSerializer(delivery, data=delivery_data)
            serializer.is_valid(raise_exception=True)
            updated_delivery = delivery_update(delivery, serializer.validated_data)
            response_data = DeliveryOutputSerializer(updated_delivery).data
            return Response(response_data)
        else:
            return Response("Erreur: la livraison demandée n'existe pas", status=status.HTTP_404_NOT_FOUND)


class DeliveryConfirmObjectAPI(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, delivery_id):
        delivery = delivery_get_object(delivery_id)
        delivery_status = request.data.get("status")
        delivery_data = request.data.get("delivery")
        delivery_data["order"] = delivery_data["order"]["order_id"]
        delivery_data["worksite"] = delivery_data["worksite"]["worksite_id"]
        delivery_data["real_date_time"] = datetime.datetime.now().isoformat()
        delivery_data["status"] = delivery_status
        print(delivery_data)
        if delivery:
            serializer = DeliveryInputSerializer(delivery, data=delivery_data)
            if serializer.is_valid():
                updated_delivery = delivery_update(delivery, serializer.validated_data)

                confirmed_delivery = delivery_confirm(updated_delivery)
                if confirmed_delivery:
                    response_data = DeliveryOutputSerializer(updated_delivery).data
                    return Response(response_data)
                else:
                    return Response({"message": "Erreur lors de la confirmation de la livraison"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"message": "Erreur: données non valides"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message": "Erreur: la livraison demandée n'existe pas"}, status=status.HTTP_404_NOT_FOUND)


class DeliveryLinesCreateObject(APIView):
    def post(self, request):
        delivery = request.data.get("delivery")
        delivery_lines_data = request.data.get("delivery_lines")
        delivery_lines_instance = delivery_lines_create(delivery_lines_data, delivery_id=delivery["delivery_id"])
        if delivery_lines_instance:
            return Response(delivery_lines_instance, status=status.HTTP_201_CREATED)
        else:
            return Response("Erreur avec l'enregistrement des produits", status=status.HTTP_400_BAD_REQUEST)


class DeliveryDeleteObjectAPI(CustomPermissionMixin, APIView):
    def delete(self, request, delivery_id):
        if self.has_permission(request, self):
            delivery = delivery_get_object(delivery_id)
            delete = delivery_delete(delivery)
            if delete:
                return Response("Suppression de la livraison")
            else:
                return Response("Erreur dans la suppression de la livraison", status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("Permission denied", status=status.HTTP_403_FORBIDDEN)


class DeliveryLinesDeleteObject(CustomPermissionMixin, APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, delivery_id):
        delete = delivery_lines_delete(delivery_id)
        if delete:
            return Response("Suppression des lignes de livraison")
        else:
            return Response("Erreur dans le suppression des lignes de livraison", status=status.HTTP_400_BAD_REQUEST)
