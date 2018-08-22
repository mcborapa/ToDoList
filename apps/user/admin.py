from django.contrib import admin
from apps.user.models import User, Things

admin.site.register(User)
admin.site.register(Things)