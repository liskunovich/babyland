from django.contrib import admin
from .models import Client, OrderRequest, Day


# Register your models here.

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Client._meta.fields]


@admin.register(OrderRequest)
class OrderRequestAdmin(admin.ModelAdmin):
    list_display = [field.name for field in OrderRequest._meta.get_fields()]


@admin.register(Day)
class WeekAdmin(admin.ModelAdmin):
    list_display = ["day", "is_workday"]
