from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import ugettext_lazy as _
from apps.basemodel.models import BaseManager


class CustomUserManager(BaseManager, BaseUserManager):
    '''
    Custom user model manager where email is the unique identifier
    for authentication instead of usernames.
    '''
    def create_user(self, email, password, **kwargs):
        if not email:
            raise ValueError(_('Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **kwargs):
        kwargs.setdefault('is_staff', True)
        kwargs.setdefault('is_superuser', True)
        kwargs.setdefault('is_active', True)

        if kwargs.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True'))
        if kwargs.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have us_superuser=True'))
        return self.create_user(email, password, **kwargs)
