from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from ..permissions.CRUDpermissions import CustomPermissionMixin
from .serializers import StockOutputSerializer, MaxStockOutputSerializer
from .selectors import get_stocks_for_worksite, get_max_stocks_for_worksite
from .services import worksite_max_stock_update_or_create


class WorksiteStockViewListAPI(CustomPermissionMixin, APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, worksite_id):
        stocks = get_stocks_for_worksite(worksite_id=worksite_id)
        if stocks:
            serializer = StockOutputSerializer(stocks, many=True)
            return Response(serializer.data)
        else:
            return Response({"message": "Erreur dans la récupération du stock"}, status=status.HTTP_404_NOT_FOUND)


class WorksiteMaxStockViewListAPI(CustomPermissionMixin, APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, worksite_id):
        stocks = get_max_stocks_for_worksite(worksite_id=worksite_id)
        if stocks:
            serializer = MaxStockOutputSerializer(stocks, many=True)
            return Response(serializer.data)
        else:
            return Response({"message": "Erreur dans la récupération du stock"}, status=status.HTTP_404_NOT_FOUND)


class WorksiteMaxStockCreateAPI(CustomPermissionMixin, APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        stocks_data = request.data.get("worksite_max_stock")
        print(stocks_data)
        stocks = []
        for stock_data in stocks_data:
            stock = worksite_max_stock_update_or_create(
                worksite_id=stock_data["worksiteId"], product=stock_data["product"], quantity=stock_data["quantity"]
            )
            print(stock)
            if stock is not None:
                stocks.append(stock)
            else:
                return Response({"message": "Erreur dans la création du stock"}, status=status.HTTP_400_BAD_REQUEST)
        serializer = MaxStockOutputSerializer(stocks, many=True)
        return Response(serializer.data)
