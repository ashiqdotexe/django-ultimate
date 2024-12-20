from django.db import models
from django.contrib.contenttypes.models import ContentType
"""
Generic relationship
"""
class Tag(models.Model):
    label = models.CharField(max_length=255)

class TagItem(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType,on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
