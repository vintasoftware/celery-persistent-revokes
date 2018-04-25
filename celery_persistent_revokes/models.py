from django.db import models


class CeleryTaskRevoke(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
