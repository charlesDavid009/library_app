from django.contrib import admin
from .models import MyUser


# Register your models here.



class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'first_name', 'last_name', 'email']

    search_feild = ['username']

    class Meta:
        model = MyUser


admin.site.register(MyUser, UserAdmin)
