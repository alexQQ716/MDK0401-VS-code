from django.urls import path
from .views import summary_api
urlpatterns = [path('api/summary/', summary_api, name='summary-api')]
