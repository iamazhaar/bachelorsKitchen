from django.contrib import admin
from . import models

# Register your models here.

@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    list_display = ["email", "name", "role", "active_status", "date_joined"]
    list_filter = ["role", "is_active"]
    list_per_page = 10
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



@admin.register(models.Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ["user_email", "user_name", "phone", "gender", "default_address", "created_at"]
    list_select_related = ["user", "default_address"]
    list_per_page = 20
    list_filter = ["gender", "created_at"]
    search_fields = ["user__email", "phone", "user__first_name", "user__last_name"]
    ordering = ["created_at"]

    @admin.display(ordering="user__first_name", description="Name")
    def user_name(self, profile):
        return f"{profile.user.first_name} {profile.user.last_name}".strip()

    @admin.display(ordering="user__email", description="Email")
    def user_email(self, profile):
        return profile.user.email