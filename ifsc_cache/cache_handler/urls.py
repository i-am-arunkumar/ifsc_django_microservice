from django.urls import path, include
from rest_framework import routers
from . import views

urlpatterns = [
    path('ifsc/<str:id>/', views.ifsc, name="ifsc" ),
    path('leaderboard/', views.leaderboard, name="leaderboard"),
    path('statistics/',views.statistics, name="statistics"),
    path('api-auth/', include('rest_framework.urls')),
]
