from django.db import models


class Title(models.Model):
    title = models.CharField(max_length=64)
    overview = models.TextField(blank=True)
    release_date = models.DateTimeField(null=True)
    tmdb_id = models.IntegerField(null=True)
    genre = models.ManyToManyField("Genre", related_name="genres", blank=True)

class Genre(models.Model):
    name = models.CharField(max_length=32)
    tmdb_id = models.IntegerField()

    def __str__(self):
        return self.name
