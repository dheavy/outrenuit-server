from django.db import models
from apps.basemodel.models import BaseModel
from apps.dreams.models import Dream


class Interpretation(BaseModel):
    dream = models.OneToOneField(Dream, on_delete=models.CASCADE)
    body = models.TextField(blank=True)

    def __str__(self):
        return 'id: {id}, dream: {dream}'.format(
            id=self.pk,
            dream=self.dream.pk
        )
