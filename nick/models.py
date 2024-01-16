from django.db import models


class Title(models.Model):
    MEDIA_TYPE_CHOICES = [
        ("MV", "Movie"),
        ("TV", "TV"),
    ]

    title = models.CharField(max_length=128, blank=True)
    overview = models.TextField(blank=True)
    release_date = models.DateField(null=True)
    tmdb_id = models.IntegerField(null=True)
    genre = models.ManyToManyField("Genre", related_name="movies", blank=True)
    role = models.CharField(max_length=128, blank=True)
    character = models.CharField(max_length=128, blank=True)
    media_type = models.CharField(max_length=2, choices=MEDIA_TYPE_CHOICES, blank=True)
    poster_path = models.URLField(max_length=200, blank=True)
    budget = models.IntegerField(null=True)
    revenue = models.IntegerField(null=True)
    runtime = models.IntegerField(null=True)
    status = models.CharField(max_length=16, blank=True)
    tagline = models.CharField(max_length=128, blank=True)
    keywords = models.ManyToManyField("Keyword", related_name="keywords", blank=True)
    companies = models.ManyToManyField("Company", related_name="companies", blank=True)
    director = models.ManyToManyField("Director", related_name="directed", blank=True)
    certification = models.CharField(max_length=16, blank=True)
    vote_average = models.FloatField(null=True)
    role_type = models.CharField(max_length=16, blank=True)

    def __str__(self):
        return self.title


class Genre(models.Model):
    name = models.CharField(max_length=32, verbose_name="genre")
    tmdb_id = models.IntegerField()

    def __str__(self):
        return self.name


class Keyword(models.Model):
    tmdb_id = models.IntegerField()
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name


class Company(models.Model):
    tmdb_id = models.IntegerField()
    name = models.CharField(max_length=32)

    class Meta:
        verbose_name_plural = 'companies'

    def __str__(self):
        return self.name


class Director(models.Model):
    tmdb_id = models.IntegerField()
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name
