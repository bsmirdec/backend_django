from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .serializers import CategoryOutputSerializer, TypeOutputSerializer, ProductOutputSerializer
from .selectors import get_category_list, get_type_list, get_product_list


class CategoryViewListAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        categories = get_category_list()
        serializer = CategoryOutputSerializer(categories, many=True)
        return Response(serializer.data)


class TypeViewListAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        types = get_type_list()
        serializer = TypeOutputSerializer(types, many=True)
        return Response(serializer.data)


class ProductViewListAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        products = get_product_list()
        serializer = ProductOutputSerializer(products, many=True)
        return Response(serializer.data)
