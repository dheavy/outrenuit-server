from django.db import models
from apps.users.models import User
from apps.basemodel.models import BaseModel
from django.utils.translation import ugettext_lazy as _


class Dream(BaseModel):

    class Typology(models.TextChoices):
        SLEEP = 'SLP', _('Sleep')
        DAYDREAM = 'DDM', _('Daydream')
        PSYCHEDELIC = 'PSY', _('Psychedelic')

    body = models.TextField()
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    label = models.CharField(max_length=25, blank=True)
    transcripted_at = models.DateField(null=True)
    type = models.CharField(
        max_length=3,
        choices=Typology.choices,
        default=Typology.SLEEP,
    )

    def __str__(self):
        return 'id: {pk}, type: {type}'.format(
            pk=self.pk,
            type=self.type
        )
