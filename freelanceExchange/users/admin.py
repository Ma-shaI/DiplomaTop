from django.contrib import admin
from .models import *
from mptt.admin import MPTTModelAdmin


class MenuItemMPTTModelAdmin(MPTTModelAdmin):
    mptt_level_indent = 20


admin.site.register(Role)
admin.site.register(Profile)
admin.site.register(Experience)
admin.site.register(LevelsEducation)
admin.site.register(Freelancer)
admin.site.register(Education)
admin.site.register(Language)
admin.site.register(Services, MenuItemMPTTModelAdmin)
