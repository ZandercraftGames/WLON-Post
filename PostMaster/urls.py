from django.urls import path
from . import views

urlpatterns = [
    # Frontend Paths
    path('', views.index, name="index"),
    path('track/<uuid:tracking_code>/', views.tracking_details, name="trackingdetails"),

    # API Paths
    path('api/', views.api, name="api"),
    path('api/track/', views.api_tracking, name="tracking"),
    path('api/track/<uuid:tracking_code>/', views.api_details, name="tracking_details")
]
