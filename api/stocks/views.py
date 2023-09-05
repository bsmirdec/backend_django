from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from ..permissions.CRUDpermissions import CustomPermissionMixin
from .serializers import StockOutputSerializer
from .selectors import get_stocks_for_worksite


class WorksiteStockViewListAPI(CustomPermissionMixin, APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, worksite_id):
        stocks = get_stocks_for_worksite(worksite_id=worksite_id)
        if stocks:
            serializer = StockOutputSerializer(stocks, many=True)
            return Response(serializer.data)
        else:
            return Response({"message": "Erreur dans la récupération du stock"}, status=status.HTTP_404_NOT_FOUND)
