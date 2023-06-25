from django.contrib import admin
from .models import *
from mptt.admin import MPTTModelAdmin


class MenuItemMPTTModelAdmin(MPTTModelAdmin):
    mptt_level_indent = 20
    prepopulated_fields = {'slug': ('name',)}


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'username')
    readonly_fields = ('id',)


class FreelancerAdmin(admin.ModelAdmin):
    list_display = ('id', 'experiences_for_freelance')
    readonly_fields = ('id',)


admin.site.register(Role)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Experience)
admin.site.register(Freelancer, FreelancerAdmin)
admin.site.register(Education)
admin.site.register(Language)
admin.site.register(Customer)
admin.site.register(StartWork)
admin.site.register(EndWork)
admin.site.register(Services, MenuItemMPTTModelAdmin)
admin.site.register(Message)
