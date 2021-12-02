from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('refresh', views.refresh),
    path('check/', views.check_solutions),
]
