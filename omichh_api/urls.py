from django.contrib import admin
from django.urls import path, include

#Django REST framework
from rest_framework.routers import DefaultRouter

# Views
from participants.views.participant import ParticipantViewSet

router = DefaultRouter()
router.register(r'participants', ParticipantViewSet, basename='participants' )

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls))
]
