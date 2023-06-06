from django.contrib import admin
from .models import *
from mptt.admin import MPTTModelAdmin


class MenuItemMPTTModelAdmin(MPTTModelAdmin):
    mptt_level_indent = 20
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Role)
admin.site.register(Profile)
admin.site.register(Experience)
admin.site.register(Freelancer)
admin.site.register(Education)
admin.site.register(Language)
admin.site.register(Customer)
admin.site.register(StartWork)
admin.site.register(EndWork)
admin.site.register(Services, MenuItemMPTTModelAdmin)
