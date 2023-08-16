from .CRUDpermissions import get_permissions_for_model, add_permissions_to_dict

from ..employees.models import Employee
from ..worksites.models import Worksite

MODELS = [Employee, Worksite]

PERMISSIONS = {}

for model in MODELS:
    model_name = model.__name__.lower()
    model_permissions = get_permissions_for_model(model_name=model_name)
    add_permissions_to_dict(model_permissions, PERMISSIONS)
