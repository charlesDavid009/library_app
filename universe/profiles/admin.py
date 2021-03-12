from django.contrib import admin
from .models import (
    Profile,
    Follow
)

# Register your models here.


class FollowProfileAdmin(admin.TabularInline):
    model = Follow


class ProfileAdmin(admin.ModelAdmin):
    inlines = [FollowProfileAdmin]
    list_display = ['user', 'first_name', 'last_name', 'nationality']

    search_feild = ['user']

    class Meta:
        model = Profile


admin.site.register(Profile, ProfileAdmin)
