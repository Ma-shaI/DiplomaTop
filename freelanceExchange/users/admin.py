from django.contrib import admin
from .models import Experience, LevelsEducation, Freelancer, Education, Languages, Skill, Services, Language
from mptt.admin import MPTTModelAdmin


class MenuItemMPTTModelAdmin(MPTTModelAdmin):
    mptt_level_indent = 20


admin.site.register(Experience)
admin.site.register(LevelsEducation)
admin.site.register(Freelancer)
admin.site.register(Education)
admin.site.register(Languages)
admin.site.register(Skill)
admin.site.register(Language)
admin.site.register(Services, MenuItemMPTTModelAdmin)
