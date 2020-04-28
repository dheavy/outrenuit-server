from django.db import models
from apps.users.models import User
from apps.basemodel.models import BaseModel
from django.utils.translation import ugettext_lazy as _


class Dream(BaseModel):
    class Typology(models.TextChoices):
        SLEEP = 'sleep', _('Sleep')
        DAYDREAM = 'daydream', _('Daydream')
        PSYCHEDELIC = 'psychedelic', _('Psychedelic')
        OTHER = 'other', _('Other')

    text = models.TextField(verbose_name=_('dream content'), blank=True)
    title = models.CharField(max_length=25, blank=True, verbose_name=_('title or identifying label'))
    transcripted_at = models.DateField(blank=True, null=True, verbose_name=_('transcription date'))
    dreamer = models.ForeignKey(
        User,
        null=True,
        on_delete=models.CASCADE,
        related_name='dreams',
        verbose_name=_('dreamer')
    )
    type = models.CharField(
        verbose_name=_('dream type'),
        max_length=25,
        choices=Typology.choices,
        default=Typology.SLEEP,
    )

    def __str__(self):
        return _(
            'Dream - id: %(pk)s, dreamer: %(dreamer)s, type: %(type)s, title: %(title)s, ' +
            'transcription date: %(trans)s, text: %(text)s'
        ) % {
            'pk': self.pk,
            'dreamer': bool(self.dreamer.profile.username) and self.dreamer.profile.username or self.dreamer.pk,
            'type': self.get_type_display(),
            'title': self.title,
            'trans': self.transcripted_at,
            'text': self.excerpt(self.text)
        }
