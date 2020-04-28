from rest_framework import viewsets
from .models import Dream
from .serializers import DreamSerializer


class DreamViewSet(viewsets.ModelViewSet):
    serializer_class = DreamSerializer
    queryset = Dream.objects.prefetch_related(
        'interpretations'
    ).prefetch_related(
        'observations'
    ).prefetch_related(
        'slips'
    ).all()
