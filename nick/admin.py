from django.contrib import admin
from .models import Title, Genre


class TitleAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "release_date", "media_type", "role", "get_genres")
    list_filter = ("media_type", "role")
    search_fields = ("title", "id", "media_type", "role")
    filter_horizontal = ("genre",)

class GenreAdmin(admin.ModelAdmin):
    list_display = ("id", "name",)
    filter_horizontal = ("movies",)

admin.site.register(Title, TitleAdmin)
admin.site.register(Genre, GenreAdmin)
