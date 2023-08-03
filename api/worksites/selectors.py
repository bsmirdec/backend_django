from .models import Worksite


def worksite_list():
    return Worksite.objects.all()


def worksite_get(pk):
    try:
        worksite = Worksite.objects.get(pk=pk)
        return worksite
    except Worksite.DoesNotExist:
        return None
