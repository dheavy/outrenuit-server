from rest_framework import serializers
from .models import User, Profile


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['username', 'bio', 'location', 'age']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'profile']

    profile = ProfileSerializer(read_only=True)


class UserWithDreamsSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + ['dreams']

    dreams = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='dream-detail'
    )
