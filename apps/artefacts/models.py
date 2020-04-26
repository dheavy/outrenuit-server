from django.db import models
from apps.basemodel.models import BaseModel
from apps.dreams.models import Dream
from django.utils.translation import ugettext_lazy as _


class FreudianSlip(BaseModel):
    dream = models.ForeignKey(Dream, verbose_name=_('dream'), on_delete=models.CASCADE)
    meant = models.CharField(max_length=255, blank=True, verbose_name=_('what was meant'))
    slipped = models.CharField(max_length=255, blank=True, verbose_name=_('slipped'))
    snippet_start = models.IntegerField(
        default=0,
        verbose_name=_('Start position in original text'),
        editable=False
    )
    snippet_end = models.IntegerField(
        default=0,
        verbose_name=_('End position in original text'),
        editable=False
    )

    def __str__(self):
        return _('Freudian Slip - id: %(id)s, dream: %(dream)s, slipped: %(slipped)s, meant: %(meant)s') % {
            'id': self.pk,
            'dream': bool(self.dream.title) and self.dream.title or self.dream.pk,
            'slipped': self.slipped,
            'meant': self.meant
        }


class Observation(BaseModel):
    dream = models.ForeignKey(Dream, on_delete=models.CASCADE)
    text = models.TextField(blank=True)
    snippet_start = models.IntegerField(
        default=0,
        verbose_name=_('Start position in original text')
    )
    snippet_end = models.IntegerField(
        default=0,
        verbose_name=_('End position in original text')
    )

    def __str__(self):
        return _('Observation - id: %(id)s, dream: %(dream)s, text: %(text)s') % {
            'id': self.pk,
            'dream': self.dream.pk,
            'text': self.text
        }
