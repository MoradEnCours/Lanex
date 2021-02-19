from django.contrib import admin
from lanex.models import Language, UserProfile, LanguageRequest


admin.site.register(Language)
admin.site.register(LanguageRequest)
admin.site.register(UserProfile)