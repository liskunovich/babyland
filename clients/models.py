from django.db import models


class Client(models.Model):
    telegram_id = models.PositiveIntegerField(primary_key=True)
    username = models.CharField(max_length=255, null=True)
    number = models.CharField(max_length=11, null=True)
