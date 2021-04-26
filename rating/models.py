from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django_extensions.db.models import TimeStampedModel

from account.models import MyUser


class RatingElement(TimeStampedModel):
    element_type = models.CharField(max_length=50)
    score = models.SmallIntegerField(blank=True, null=True)
    comment = models.CharField(blank=True, null=True, max_length=512)

    class Meta:
        ordering = ('id', )

    def __str__(self):
        return f'{self.id} - {self.element_type} - {self.score} - {self.comment}'


class ObjectRating(TimeStampedModel):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()

    elements = models.ManyToManyField(RatingElement)

    class Meta:
        verbose_name = 'Rating'
        ordering = ('id', )
