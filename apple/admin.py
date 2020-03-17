from django.contrib import admin

# Register your models here.
from apple.models import Topic, Entry, EntryAdmin
admin.site.register(Topic)
admin.site.register(Entry, EntryAdmin)
