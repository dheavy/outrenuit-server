from django.db import models
from apps.basemodel.models import BaseModel
from apps.dreams.models import Dream
from django.utils.translation import ugettext_lazy as _


class Artefact(BaseModel):

    class Typology(models.TextChoices):
        OBSERVATION = 'OBS', _('Observation')
        FREUDIAN_SLIP = 'FRS', _('Freudian slip')
        SYMBOLS = 'SYM', _('Symbols')

    dream = models.ForeignKey(Dream, on_delete=models.CASCADE)
    body = models.TextField(blank=True)
    label = models.CharField(max_length=255, blank=True)
    label_start = models.IntegerField(
        default=0,
        help_text='Start position in original string'
    )
    label_end = models.IntegerField(
        default=0,
        help_text='End position in original string'
    )
    type = models.CharField(
        max_length=3,
        choices=Typology.choices,
        default=Typology.OBSERVATION
    )

    def __str__(self):
        return 'id: {id}, dream: {dream}, label: {label}, type: {type}'.format(
            id=self.pk,
            dream=self.dream.pk,
            label=self.label,
            type=self.type
        )
