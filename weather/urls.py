from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name="homepage"),
    path('home', views.index, name="homepage"),
    # path('graph', views.graph, name="graphPage"),
    path('infoPage', views.info),
]
