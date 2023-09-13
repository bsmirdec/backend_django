from .models import Stock, WorksiteMaxStock

from ..worksites.selectors import worksite_get


def get_stock(stock_id):
    return Stock.objects.get(pk=stock_id)


def get_stocks_for_worksite(worksite_id):
    worksite = worksite_get(pk=worksite_id)
    if worksite:
        stocks = Stock.objects.filter(worksite=worksite_id)
        return stocks
    else:
        return None


def get_max_stocks_for_worksite(worksite_id):
    worksite = worksite_get(pk=worksite_id)
    print(worksite)
    if worksite:
        max_stocks = WorksiteMaxStock.objects.filter(worksite=worksite.worksite_id)
        print(max_stocks)
        return max_stocks
    else:
        return None
