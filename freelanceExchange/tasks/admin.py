from django.contrib import admin
from .models import *


class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    readonly_fields = ('id',)


admin.site.register(Budget)
admin.site.register(Task, TaskAdmin)
admin.site.register(Work)
admin.site.register(StagesOfWork)
admin.site.register(Offers)