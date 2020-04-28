from rest_framework import serializers
from .models import Interpretation


class InterpretationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interpretation
        fields = ['id', 'interpreter', 'dream', 'text']
