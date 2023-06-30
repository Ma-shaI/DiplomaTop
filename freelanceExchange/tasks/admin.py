from django.contrib import admin
from .models import *


class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    readonly_fields = ('id',)


admin.site.register(Budget)
admin.site.register(Task, TaskAdmin)
