from django.db import models


class Client(models.Model):
    telegram_id = models.PositiveIntegerField(unique=True)
    username = models.CharField(max_length=255, null=True)
    number = models.CharField(max_length=11, null=True)

    def __str__(self):
        return self.number


class OrderRequest(models.Model):
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    children_amount = models.PositiveIntegerField()
    client = models.ForeignKey(Client, on_delete=models.DO_NOTHING, related_name='orders')
