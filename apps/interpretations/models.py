from django.db import models
from apps.basemodel.models import BaseModel
from apps.dreams.models import Dream
from django.utils.translation import ugettext_lazy as _


class Interpretation(BaseModel):
    dream = models.OneToOneField(Dream, verbose_name=_('dream'), on_delete=models.CASCADE)
    text = models.TextField(verbose_name=_('interpretation'), blank=True)

    def __str__(self):
        return _('Interpretation - id: %(pk)s, dream: %(dream)s, text: %(text)s') % {
            'pk': self.pk,
            'dream': bool(self.dream.label) and self.dream.label or self.dream.pk,
            'text': self.excerpt(self.text)
        }
