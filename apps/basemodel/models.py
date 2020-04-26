from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


class BaseManager(models.Manager):

    def __init__(self):
        super(BaseManager, self).__init__()

    def get_query_set(self):
        return super().get_queryset().exclude(soft_deleted=True)


class BaseModel(models.Model):
    '''
    Base model with timestamps, soft delete, and excerpt helper all models should inherit from.
    '''
    created_at = models.DateTimeField(editable=False, default=timezone.now)
    modified_at = models.DateTimeField(default=timezone.now)
    soft_deleted = models.BooleanField(
        default=False,
        verbose_name=_('In the trash bin')
    )

    objects = BaseManager()

    class Meta:
        abstract = True

    def __init__(self, *args, **kwargs):
        super(BaseModel, self).__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        if not self.id:
            self.created_at = timezone.now()
        self.modified_at = timezone.now()
        return super(BaseModel, self).save(*args, **kwargs)

    def delete(self, **kwargs):
        force_delete = kwargs.pop('force', False)
        if force_delete:
            self.soft_deleted = True
            self.save()
        else:
            super(BaseModel, self).delete(**kwargs)

    def excerpt(self, string, length=15, ellipsis='...'):
        return string.replace('\n', '')[:length] + ellipsis
