from .models import Worksite


def worksite_create(data):
    worksite = Worksite(**data)
    worksite.full_clean()

    worksite.save()

    return worksite


def worksite_update(worksite, data):
    for key, value in data.items():
        setattr(worksite, key, value)
    worksite.save()
    return worksite


def worksite_delete(worksite):
    worksite.delete()
