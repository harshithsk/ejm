from django.db import models
from django.core.validators import FileExtensionValidator
from django.utils import timezone
from slugger.fields import AutoSlugField


# Create your models here.

class Volume(models.Model):
    title = models.CharField(max_length=50)
    published_date = models.DateField()
    def __str__(self):
        return self.title


class PublishedJournal(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    upload = models.FileField(validators=[FileExtensionValidator(["pdf"])])
    preview_image = models.ImageField()
    slug = AutoSlugField(populate_from="name", unique=True, editable=False)
    volume = models.ForeignKey(Volume, on_delete=models.SET_NULL, null=True)
    def published_date(self):
        if self.volume is None:
            return ""
        return self.volume.published_date

    def __str__(self):
        return self.name
