from rest_framework import viewsets
from .models import Interpretation
from .serializers import InterpretationSerializer


class InterpretationViewSet(viewsets.ModelViewSet):
    serializer_class = InterpretationSerializer
    queryset = Interpretation.objects.select_related(
        'dream'
    ).select_related(
        'interpreter'
    ).all()
