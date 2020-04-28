from rest_framework import serializers
from apps.artefacts.serializers import FreudianSlipSerializer, ObservationSerializer
from apps.interpretations.serializers import InterpretationSerializer
from .models import Dream


class DreamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dream
        fields = [
            'id', 'text', 'title', 'type', 'transcripted_at', 'created_at',
            'dreamer', 'observations', 'interpretations', 'slips'
        ]

    slips = FreudianSlipSerializer(many=True, read_only=True)
    observations = ObservationSerializer(many=True, read_only=True)
    interpretations = InterpretationSerializer(many=True, read_only=True)
