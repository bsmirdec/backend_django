from .models import Category, Type, Product


def get_category_list():
    return Category.objects.all()


def get_type_list():
    return Type.objects.all()


def get_product_list():
    return Product.objects.all()
