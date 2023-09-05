import json
from rest_framework.permissions import IsAdminUser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from ..permissions.CRUDpermissions import CustomPermissionMixin
from .serializers import RequestSerializer, OrderOutputSerializer, OrderLineOutputSerializer
from .services import order_create, order_lines_create, order_lines_delete, order_update, order_delete
from .selectors import get_threshold_for_order, order_get_list, order_lines_get_list, order_get_object
from .order_validation import order_confirm


class RequestViewListAPI(CustomPermissionMixin, APIView):
    def get(self, request):
        if self.has_permission(request, self):
            pass
        else:
            return Response("Permission denied", status=status.HTTP_403_FORBIDDEN)


class OrderViewListAPI(CustomPermissionMixin, APIView):
    def get(self, request, employee_id):
        orders = order_get_list(employee_id)
        if orders:
            serializer = OrderOutputSerializer(orders, many=True)
            return Response(serializer.data)
        else:
            return Response({"message": "Pas de commandes"}, status=status.HTTP_404_NOT_FOUND)


class OrderLinesViewListAPI(CustomPermissionMixin, APIView):
    def get(self, request, order_id):
        order_lines = order_lines_get_list(order_id)
        serializer = OrderLineOutputSerializer(order_lines, many=True)
        return Response(serializer.data)


class RetourViewListAPI(APIView):
    pass


class RequestRetrieveObjectAPI(CustomPermissionMixin, APIView):
    def get(self, request):
        if self.has_permission(request, self):
            pass
        else:
            return Response("Permission denied", status=status.HTTP_403_FORBIDDEN)


class OrderRetrieveObjectAPI(RequestRetrieveObjectAPI):
    def get(self, request, order_id):
        order = order_get_object(order_id)
        if order:
            response_data = OrderOutputSerializer(order).data
            return Response(response_data)
        else:
            return Response("Erreur dans la récupération de la commande", status=status.HTTP_404_NOT_FOUND)


class RetourRetrieveObjectAPI(APIView):
    pass


class RequestCreateObjectAPI(CustomPermissionMixin, APIView):
    def post(self, request):
        if self.has_permission(request, self):
            pass
        else:
            return Response("Permission denied", status=status.HTTP_403_FORBIDDEN)


class OrderCreateObjectAPI(RequestCreateObjectAPI):
    def post(self, request):
        order_data = request.data.get("order")
        order_lines_data = request.data.get("order_lines")
        order_lines_data = json.loads(order_lines_data)
        employee_id = request.data.get("employee_id")

        # Définition du seuil de commande basé sur les types de produits commandés
        threshold = get_threshold_for_order(order_lines_data)
        order_data["threshold"] = threshold

        # Création de la commande
        order_serializer = RequestSerializer(data=order_data)
        if order_serializer.is_valid():
            order_instance = order_create(order_serializer.validated_data, employee_id)
            order_data = OrderOutputSerializer(order_instance).data

            # Création des lignes de commandes associées
            order_lines_data = order_lines_create(order_lines_data, order_id=order_instance.order_id)
            if order_lines_data:
                response_dict = {
                    "order_data": order_data,
                    "order_lines": order_lines_data,
                }
                return Response(response_dict, status=status.HTTP_201_CREATED)
            else:
                return Response("Erreur avec l'enregistrement des produits", status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(order_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RequestUpdateObjectAPI(CustomPermissionMixin, APIView):
    def put(self, request):
        if self.has_permission(request, self):
            pass
        else:
            return Response("Permission denied", status=status.HTTP_403_FORBIDDEN)


class OrderUpdateObjectAPI(RequestUpdateObjectAPI):
    def put(self, request, order_id):
        order = order_get_object(order_id)
        order_data = request.data.get("order")
        print(order_data)
        order_data["worksite"] = order_data["worksite"]["worksite_id"]
        employee_id = request.data.get("employee_id")
        if order:
            serializer = RequestSerializer(order, data=order_data)
            serializer.is_valid(raise_exception=True)
            updated_order = order_update(order, serializer.validated_data, employee_id)
            response_data = OrderOutputSerializer(updated_order).data
            return Response(response_data)
        else:
            return Response("Erreur: la commande demandée n'existe pas", status=status.HTTP_404_NOT_FOUND)


class OrderConfirmAPI(APIView):
    permissions_classes = [IsAdminUser]

    def get(self, request, order_id):
        order = order_get_object(order_id=order_id)
        confirmed = order_confirm(order)
        if confirmed:
            return Response({"message": "Commande confirmée, Livraison créée"}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Erreur dans la confirmation de la commande"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class OrderLinesCreateObject(RequestCreateObjectAPI):
    def post(self, request):
        order = request.data.get("order")
        print(order)
        order_lines_data = request.data.get("order_lines")
        print(order_lines_data)
        order_lines_instance = order_lines_create(order_lines_data, order_id=order["order_id"])
        if order_lines_instance:
            return Response(order_lines_instance, status=status.HTTP_201_CREATED)
        else:
            return Response("Erreur avec l'enregistrement des produits", status=status.HTTP_400_BAD_REQUEST)


class RequestDeleteObjectAPI(CustomPermissionMixin, APIView):
    def delete(self, request):
        if self.has_permission(request, self):
            pass
        else:
            return Response("Permission denied", status=status.HTTP_403_FORBIDDEN)


class OrderDeleteObjectAPI(RequestDeleteObjectAPI):
    def delete(self, request, order_id):
        order = order_get_object(order_id)
        delete = order_delete(order)
        if delete:
            return Response("Suppression de la commande")
        else:
            return Response("Erreur dans la suppression de la commande", status=status.HTTP_400_BAD_REQUEST)


class OrderLinesDeleteObject(RequestDeleteObjectAPI):
    def delete(self, request, order_id):
        delete = order_lines_delete(order_id)
        if delete:
            return Response("Suppression des lignes de commande")
        else:
            return Response("Erreur dans le suppression des lignes de commande", status=status.HTTP_400_BAD_REQUEST)
