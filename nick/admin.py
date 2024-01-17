from django.contrib import admin
from .models import *


class TitleAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "status",
        "role_type",
        "role",
        "release_date",
        "media_type",
        "status",
        "vote_average",
        "genres_list",
    )
    list_filter = ("media_type", "role_type", "role", "status", "genre__name")
    search_fields = ("title", "id", "media_type", "role", "genre__name")
    filter_horizontal = ("genre", "keywords", "companies", "director")


class GenreAdmin(admin.ModelAdmin):
    list_display = ("name", "id", "movies_list")
    list_filter = ("movies__genre", "movies__media_type", "movies__status")


class KeywordAdmin(admin.ModelAdmin):
    list_display = ("name", "tmdb_id", "get_titles")
    search_fields = ("name",)

    def get_titles(self, obj):
        return list(obj.keywords.all())


class CompanyAdmin(admin.ModelAdmin):
    list_display = ("name", "tmdb_id")
    search_fields = ("name",)


class DirectorAdmin(admin.ModelAdmin):
    list_display = ("name", "tmdb_id", "get_titles")
    search_fields = ("name",)

    def get_titles(self, obj):
        return list(obj.directed.all())


admin.site.register(Title, TitleAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Keyword, KeywordAdmin)
admin.site.register(Company, CompanyAdmin)
admin.site.register(Director, DirectorAdmin)
