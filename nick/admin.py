from django.contrib import admin
from .models import *
from django.db.models import Count

"""Not much here, just adding things to be useful during debugging in the admin page, however I will describe some tricks"""


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
        "certification",
    )
    list_filter = ("media_type", "certification", "role_type", "role", "status", "genre__name") #genre__name filters the foreign keyword by the name, so it can be used!
    search_fields = ("title", "id", "media_type", "role", "genre__name")
    filter_horizontal = ("genre", "keywords", "companies", "director")


class GenreAdmin(admin.ModelAdmin):
    list_display = ("name", "id", "movies_list", "total_titles")
    list_filter = ("movies__genre", "movies__media_type", "movies__status")

    """Two next functions enable me to check number of movies by annotating (reverse relation). Useful for testing some queries and checking against the admin panel"""
    def get_queryset(self, request):
        return super().get_queryset(request).annotate(titles_count=Count("movies"))
    
    @admin.display(description='Total Titles', ordering='titles_count')
    def total_titles(self, obj):
        return obj.movies.count()


class KeywordAdmin(admin.ModelAdmin):
    list_display = ("name", "tmdb_id", "get_titles", "total_titles")
    search_fields = ("name",)
    

    def get_titles(self, obj):
        return list(obj.keywords.all())
    
    
    def get_queryset(self, request):
        return super().get_queryset(request).annotate(titles_count=Count("keywords"))
    
    @admin.display(description='Total Titles', ordering='titles_count')
    def total_titles(self, obj):
        return obj.keywords.count()



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
