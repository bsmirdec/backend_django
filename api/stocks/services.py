from .models import Stock
from .serializers import StockInputSerializer
from .selectors import get_stock


def stock_create(worksite, delivery_line):
    try:
        # Essayez de récupérer le Stock existant pour le produit et le site de travail
        stock = Stock.objects.get(worksite=worksite, product=delivery_line.product.product_id)

        # Mise à jour de la quantité en ajoutant la quantité de la ligne de livraison
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
        print(stock_serializer.initial_data)
        if stock_serializer.is_valid():
            print("succès")
            stock = Stock.objects.create(**stock_serializer.validated_data)
            return True
        else:
            print("Non")
            return False


def stock_delete(stock_id):
    stock = get_stock(stock_id)
    stock.delete()
