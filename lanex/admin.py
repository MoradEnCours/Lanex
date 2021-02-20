from django.contrib import admin
from lanex.models import Language, LanguageRequest, UserProfile

class LanguageAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}

class RequestAdmin(admin.ModelAdmin):
    list_display = ['title', 'language', 'url']

admin.site.register(Language, LanguageAdmin)
admin.site.register(LanguageRequest, RequestAdmin)
admin.site.register(UserProfile)