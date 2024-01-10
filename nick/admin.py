from django.contrib import admin
from .models import Title, Genre


class TitleAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "release_date", "media_type", "credit_type", "role", "get_genres")
    list_filter = ("credit_type", "media_type")
    search_fields = ("title", "id", "media_type")
    filter_horizontal = ("genre",)

class GenreAdmin(admin.ModelAdmin):
    list_display = ("id", "name",)
    filter_horizontal = ("movies",)

admin.site.register(Title, TitleAdmin)
admin.site.register(Genre, GenreAdmin)
