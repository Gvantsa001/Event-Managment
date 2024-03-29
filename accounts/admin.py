from django.contrib import admin
from accounts.models import User
from events.models import Event


admin.site.register(User)
admin.site.register(Event)
