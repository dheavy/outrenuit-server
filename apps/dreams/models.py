from django.db import models
from apps.users.models import User
from apps.basemodel.models import BaseModel
from django.utils.translation import ugettext_lazy as _


class Dream(BaseModel):

    class Typology(models.TextChoices):
        SLEEP = 'SLP', _('Sleep')
        DAYDREAM = 'DDM', _('Daydream')
        PSYCHEDELIC = 'PSY', _('Psychedelic')
        OTHER = 'OTH', _('Other')

    text = models.TextField(verbose_name=_('dream content'), blank=True)
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE, verbose_name=_('dreamer'))
    title = models.CharField(max_length=25, blank=True, verbose_name=_('title or identifying label'))
    transcripted_at = models.DateField(blank=True, null=True, verbose_name=_('transcription date'))
    type = models.CharField(
        verbose_name=_('dream type'),
        max_length=3,
        choices=Typology.choices,
        default=Typology.SLEEP,
    )

    def __str__(self):
        return _(
            'Dream - id: %(pk)s, user: %(user)s, type: %(type)s, title: %(title)s, ' +
            'transcription date: %(trans)s, text: %(text)s'
        ) % {
            'pk': self.pk,
            'user': bool(self.user.profile.username) and self.user.profile.username or self.user.pk,
            'type': self.get_type_display(),
            'title': self.title,
            'trans': self.transcripted_at,
            'text': self.excerpt(self.text)
        }
