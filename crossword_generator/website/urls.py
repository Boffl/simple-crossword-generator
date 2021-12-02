from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('refresh', views.refresh),
    path('website/<uuid:pk>/renew/', views.check_solutions),
]
