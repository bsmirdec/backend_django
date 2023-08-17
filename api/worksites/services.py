from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from .models import Worksite


def worksite_create(data):
    worksite = Worksite(**data)

    try:
        worksite.full_clean()
        worksite.save()
    except IntegrityError:
        raise ValidationError("Une erreur s'est produite lors de la création du Worksite.")

    return worksite


def worksite_update(worksite, data):
    for key, value in data.items():
        setattr(worksite, key, value)
    worksite.save()
    return worksite


def worksite_delete(worksite):
    worksite.delete()
