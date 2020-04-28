from rest_framework import serializers
from .models import FreudianSlip, Observation


class FreudianSlipSerializer(serializers.ModelSerializer):
    class Meta:
        model = FreudianSlip
        fields = [
            'id', 'dream', 'meant', 'slipped', 'snippet_start', 'snippet_end'
        ]


class ObservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Observation
        fields = ['id', 'dream', 'text', 'snippet_start', 'snippet_end']
