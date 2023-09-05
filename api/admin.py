from django.contrib import admin

# Register your models here.
from django.contrib import admin

from .worksites.models import Worksite
from .employees.models import Employee
from .managements.models import Management
from .notifications.models import Notification
from .products.models import Category, Type, Product
from .stocks.models import WarehouseStock, Stock
from .requests.models import Order, OrderLine
from .deliveries.models import Delivery, DeliveryLine

admin.site.register(Worksite)
admin.site.register(Employee)
admin.site.register(Management)
admin.site.register(Notification)
admin.site.register(Category)
admin.site.register(Type)
admin.site.register(Product)
admin.site.register(WarehouseStock)
admin.site.register(Stock)
admin.site.register(Order)
admin.site.register(OrderLine)
admin.site.register(Delivery)
admin.site.register(DeliveryLine)
