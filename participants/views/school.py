''' School Viewset '''

# Django REST framework
from rest_framework import mixins, viewsets

# Models
from participants.models import School

# Serializers
from participants.serializers.school import SchoolModelSerializer


class SchoolViewSet(mixins.CreateModelMixin,
                    mixins.RetrieveModelMixin,
                    viewsets.GenericViewSet):
    ''' School model viewset '''

    queryset = School.objects.all()
    serializer_class = SchoolModelSerializer
