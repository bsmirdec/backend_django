from django.urls import path

from .views import WorksiteList, WorksiteListCreate, WorksiteDetail, ClientList, ClientDetail


urlpatterns = [
    path("worksite/", WorksiteList.as_view(), name="worksitelist"),
    path("worksite/create/", WorksiteListCreate.as_view(), name="worksitelistcreate"),
    path("worksite/<int:pk>/", WorksiteDetail.as_view(), name="worksitedetail"),
    path("client/", ClientList.as_view(), name="clientlist"),
    path("client/<int:pk>/", ClientDetail.as_view, name="clientdetail"),
]