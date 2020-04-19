from django.db import models
from apps.basemodel.models import BaseModel
from django.utils.translation import ugettext_lazy as _


class Dream(BaseModel):

    class Typology(models.TextChoices):
        SLEEP = 'SLP', _('Sleep')
        DAYDREAM = 'DDM', _('Daydream')
        PSYCHEDELIC = 'PSY', _('Psychedelic')

    body = models.TextField()
    type = models.CharField(
        max_length=3,
        choices=Typology.choices,
        default=Typology.SLEEP,
    )

    def __str__(self):
        return 'Dream (id: {pk}, type: {type})'.format(
            pk=self.pk,
            type=self.type
        )
