from unidecode import unidecode

from .models import CustomUser
from api.employees.models import Employee


def user_create(data):
    password = data.pop("password", None)
    user = CustomUser.objects.create(**data)
    if password is not None:
        user.set_password(password)
    user.full_clean()
    user.save()
    return user


def normalize_name(name):
    normalized_name = unidecode(name.lower())
    return normalized_name


def user_link_to_employee(user_id, first_name, last_name):
    """Une fois l'utilisateur créer, on fusionne son instance d'employé avec les nom et prénom qu'il aura saisis"""
    try:
        user = CustomUser.objects.get(user_id=user_id)
        normalize_first_name = normalize_name(first_name)
        normalize_last_name = normalize_name(last_name)
        employee = Employee.objects.get(first_name__iexact=normalize_first_name, last_name__iexact=normalize_last_name)
        user.employee = employee
        if employee.position == "administrator":
            user.is_staff = True
        user.save()
        return user  # A cet endroit, il faut envoyer une notification aux administrateur pour valider le profil créé
    except Employee.DoesNotExist:
        return None


def user_confirmation(user):
    """A réaliser par un admin, une fois la fusion user/employé effectuée
    passer la status utilisateur is_validated à True pour permettre l'utilisation du compte"""
    pass


def user_update(user, data):
    for key, value in data.items():
        setattr(user, key, value)
    user.save()
    return user


def user_delete(user):
    user.delete()


# from django.core.mail import send_mail
# from ..contact_admin import EMAIL_ADMIN

# def send_email_to_admin(subject, message, from_email):
#     send_mail(subject=subject, message=message, from_email=from_email, recipient_list=[EMAIL_ADMIN])


# def send_confirmation_email(user, email):
#     subject = f"Confirmation création du compte de {user.email}"
#     message = "Merci de bien vouloir aller valider le compte"
#     send_email_to_admin(subject=subject, message=message, from_email=email)
