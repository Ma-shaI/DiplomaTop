from django.contrib import admin
from .models import *


class TalentAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    readonly_fields = ('id',)


admin.site.register(Talent, TalentAdmin)
admin.site.register(Skills)
admin.site.register(HourlyRate)
