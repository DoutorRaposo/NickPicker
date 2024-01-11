from django.contrib import admin
from .models import *


class TitleAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "status","release_date", "media_type", "role", "get_genres")
    list_filter = ("media_type", "role", "status")
    search_fields = ("title", "id", "media_type", "role")
    filter_horizontal = ("genre", "keywords", "companies")

class GenreAdmin(admin.ModelAdmin):
    list_display = ("name", "id", )
    filter_horizontal = ("movies",)

class KeywordAdmin(admin.ModelAdmin):
    list_display = ("name", "tmdb_id")

class CompanyAdmin(admin.ModelAdmin):
    list_display = ("name", "tmdb_id")

admin.site.register(Title, TitleAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Keyword, KeywordAdmin)
admin.site.register(Company, CompanyAdmin)
