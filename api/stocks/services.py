from .models import Stock, WorksiteMaxStock
from .serializers import StockInputSerializer
from .selectors import get_stock


def stock_create(worksite, delivery_line):
    try:
        # Le produit existe-t'il déjà sur le chantier ?
        stock = Stock.objects.get(worksite=worksite, product=delivery_line.product.product_id)
        stock.quantity += delivery_line.quantity
        stock.save()

        return True
    except Stock.DoesNotExist:
        # Si le Stock n'existe pas encore, créez-en un nouveau
        stock_data = {
            "worksite": worksite,
            "product": delivery_line.product.product_id,
            "quantity": delivery_line.quantity,
        }
        stock_serializer = StockInputSerializer(data=stock_data)
        if stock_serializer.is_valid():
            print("succès")
            stock = Stock.objects.create(**stock_serializer.validated_data)
            return True
        else:
            print("Non")
            return False


def worksite_max_stock_update_or_create(worksite_id, product, quantity):
    try:
        stock = WorksiteMaxStock.objects.get(worksite=worksite_id, product=product["product_id"])
        stock.quantity = quantity
        stock.save()

        return stock

    except WorksiteMaxStock.DoesNotExist:
        stock_data = {
            "worksite": worksite_id,
            "product": product["product_id"],
            "quantity": quantity,
        }
        stock_serializer = StockInputSerializer(data=stock_data)
        if stock_serializer.is_valid():
            stock = WorksiteMaxStock.objects.create(**stock_serializer.validated_data)
            return stock
        else:
            return None


def stock_delete(stock_id):
    stock = get_stock(stock_id)
    stock.delete()
