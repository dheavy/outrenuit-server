from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver
from random import choice
from string import ascii_lowercase, digits
from random_username.generate import generate_username
from apps.basemodel.models import BaseModel
from .managers import CustomUserManager


def generate_random_username(length=5, chars=ascii_lowercase + digits, split=4, delimiter=''):
    username = generate_username(1)[0] + ''.join(
        [choice(chars) for i in range(length)]
    )
    if split:
        username = delimiter.join(
            [username[start:start + split] for start in range(0, len(username), split)]
        )
    try:
        Profile.objects.get(username=username)
        return generate_random_username(
            length=length, chars=chars, split=split, delimiter=delimiter
        )
    except Profile.DoesNotExist:
        return username


class User(BaseModel, AbstractUser):
    username = None
    email = models.EmailField(verbose_name=_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return _(
            'User - id: %(pk)s, username: %(username)s, is staff member: %(staff)s, is administrator: %(admin)s'
        ) % {
            'pk': self.pk,
            'username': self.profile.username,
            'staff': self.is_staff,
            'admin': self.is_superuser
        }


class Profile(BaseModel):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name=_('related user')
    )
    username = models.CharField(
        verbose_name=_('username'),
        max_length=30,
        blank=True,
        unique=True
    )
    bio = models.TextField(
        verbose_name=_('bio'),
        max_length=500,
        blank=True
    )
    location = models.CharField(
        verbose_name=_('location'),
        max_length=30,
        blank=True
    )
    age = models.IntegerField(verbose_name=_('age'), blank=True, null=True)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            username = generate_random_username()
            Profile.objects.create(user=instance, username=username)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

    def __str__(self):
        return _(
            'User profile - id %(pk)s, user id: %(userid)s, username: %(username)s, age: %(age)s, bio: %(bio)s'
        ) % {
            'pk': self.pk,
            'userid': self.user.id,
            'username': self.username,
            'age': self.age,
            'bio': self.excerpt(self.bio)
        }
