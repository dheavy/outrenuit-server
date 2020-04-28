from rest_framework import viewsets
from .serializers import UserSerializer, UserWithDreamsSerializer, ProfileSerializer
from .models import User, Profile


class UserViewSet(viewsets.ModelViewSet):
    '''
    Use URL parameter "dream" to yield related Dreams as API hyperlinks.
    e.g. /api/v1/user?dreams=true"
    '''
    queryset = User.objects.select_related('profile').prefetch_related('dreams').all()

    def get_serializer_class(self):
        if 'dreams' in self.request.query_params:
            return UserWithDreamsSerializer
        return UserSerializer


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.select_related('user')
    serializer_class = ProfileSerializer
