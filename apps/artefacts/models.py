from django.db import models
from apps.basemodel.models import BaseModel
from apps.dreams.models import Dream
from django.utils.translation import ugettext_lazy as _


class Artefact(BaseModel):

    class Typology(models.TextChoices):
        NOTES = 'NOT', _('Notes')
        FREUDIAN_SLIP = 'FRS', _('Freudian slip')
        SYMBOLS = 'SYM', _('Symbols')

    dream = models.OneToOneField(Dream, on_delete=models.CASCADE)
    body = models.TextField(blank=True)
    label = models.CharField(max_length=255, blank=True)
    type = models.CharField(
        max_length=3,
        choices=Typology.choices,
        default=Typology.NOTES
    )

    def __str__(self):
        return 'Artefact (id: {id}, dream: {dream}, label: {label}, type: {type})'.format(
            id=self.pk,
            dream=self.dream.pk,
            label=self.label,
            type=self.type
        )
