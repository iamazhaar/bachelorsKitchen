from django.contrib import admin
from . import models

# Register your models here.
@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    list_display = ["email", "name", "role", "active_status", "date_joined"]
    list_filter = ["role", "is_active"]
    ordering = ["first_name", "last_name"]
    search_fields = ["email", "first_name", "last_name"]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.only("first_name", "last_name", "email", "role", "is_active", "date_joined")

    @admin.display(ordering="first_name")
    def name(self, user):
        return f"{user.first_name} {user.last_name}".strip()
    
    def active_status(self, user):
        return user.is_active
    active_status.boolean = True
    active_status.short_description = "Active"
