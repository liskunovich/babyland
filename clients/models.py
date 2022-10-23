from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class Client(models.Model):
    telegram_id = models.PositiveIntegerField(unique=True)
    username = models.CharField(max_length=255, null=True)
    number = models.CharField(max_length=11, null=True)

    def __str__(self):
        return self.number


class Day(models.Model):
    date = models.DateField()
    total_children = models.PositiveIntegerField(default=0, validators=[
        MaxValueValidator(10),
        MinValueValidator(1)
    ])
    day = models.CharField(max_length=255)
    is_available = models.BooleanField(default=True)


class OrderRequest(models.Model):
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    children_amount = models.PositiveIntegerField(validators=[
        MaxValueValidator(10),
        MinValueValidator(1)
    ])
    day = models.ForeignKey(Day, on_delete=models.DO_NOTHING, related_name='orders')
    client = models.ForeignKey(Client, on_delete=models.DO_NOTHING, related_name='orders')
