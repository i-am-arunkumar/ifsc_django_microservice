from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'ifsc',views.IFSCViewSet, "ifsc")
router.register(r'hits',views.ApiHistoryViewset, "hits")

urlpatterns = [
    path('',include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
]
