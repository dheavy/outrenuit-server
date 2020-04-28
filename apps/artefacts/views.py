from rest_framework import viewsets
from .models import FreudianSlip, Observation
from .serializers import FreudianSlipSerializer, ObservationSerializer


class FreudianSlipViewSet(viewsets.ModelViewSet):
    serializer_class = FreudianSlipSerializer
    queryset = FreudianSlip.objects.select_related('dream').all()


class ObservationViewSet(viewsets.ModelViewSet):
    serializer_class = ObservationSerializer
    queryset = Observation.objects.select_related('dream').all()
