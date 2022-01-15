from django.contrib import admin
from django.urls import path, include

#Django REST framework
from rest_framework.routers import DefaultRouter

# Views
from participants.views.participant import ParticipantViewSet
from participants.views.school import SchoolViewSet

router = DefaultRouter()
router.register(r'participants', ParticipantViewSet, basename='participants' )
router.register(r'schools', SchoolViewSet, basename='schools')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls))
]
