from django.urls import path, include
from rest_framework import routers
from . import views

urlpatterns = [
    path('ifsc/<str:id>/', views.get_ifsc),
    path('leaderboard/', views.leaderboard),
    path('statistics/',views.statistics),
    path('api-auth/', include('rest_framework.urls')),
]
