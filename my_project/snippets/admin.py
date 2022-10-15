from django.contrib import admin

from snippets.models import UserDetails

# Register your models here.
class UserDetailAdmin(admin.ModelAdmin):
    fields = ["phone_number", "activation_key", "user"]

admin.site.register(UserDetails, UserDetailAdmin)
