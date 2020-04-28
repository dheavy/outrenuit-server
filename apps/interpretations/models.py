from django.db import models
from apps.basemodel.models import BaseModel
from apps.dreams.models import Dream
from apps.users.models import User
from django.utils.translation import ugettext_lazy as _


class Interpretation(BaseModel):
    dream = models.ForeignKey(
        Dream,
        null=True,
        related_name='interpretations',
        verbose_name=_('dream'),
        on_delete=models.CASCADE
    )
    interpreter = models.ForeignKey(
        User,
        null=True,
        related_name='interpreter',
        verbose_name=_('interpreter'),
        on_delete=models.CASCADE
    )
    text = models.TextField(verbose_name=_('interpretation'), blank=True)

    def __str__(self):
        return _('Interpretation - id: %(pk)s, dream: %(dream)s, text: %(text)s') % {
            'pk': self.pk,
            'dream': bool(self.dream.label) and self.dream.label or self.dream.pk,
            'text': self.excerpt(self.text)
        }
