from django.contrib.auth import get_user_model

from models import Worksite, WorksiteEmployee


User = get_user_model()


def create_management(data):
    worksite_id = data["worksite"]
    employees = data["employees"]

    worksite = Worksite.objects.get(id=worksite_id)

    for employee_id in employees:
        employee = None

        # Vérifier le type d'employé en fonction de la sous-classe
        if Administrator.objects.filter(user_id=employee_id).exists():
            employee = Administrator.objects.get(user_id=employee_id)
        elif SiteDirector.objects.filter(user_id=employee_id).exists():
            employee = SiteDirector.objects.get(user_id=employee_id)
        elif SiteSupervisor.objects.filter(user_id=employee_id).exists():
            employee = SiteSupervisor.objects.get(user_id=employee_id)
        elif SiteForeman.objects.filter(user_id=employee_id).exists():
            employee = SiteForeman.objects.get(user_id=employee_id)

        if employee is not None:
            # Créer une instance de Management avec les informations récupérées
            management = Management(worksite=worksite, user=employee.user)
            management.save()

        return management
