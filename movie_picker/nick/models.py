from django.db import models


class Title(models.Model):
    MEDIA_TYPE_CHOICES = [
        ("MV", "Movie"),
        ("TV", "TV"), 
    ]

    CREDIT_TYPE_CHOICES = [
        ("ACT", "Actor"),
        ("CRW", "Crew")
    ]

    title = models.CharField(max_length=128, blank=True)
    overview = models.TextField(blank=True)
    release_date = models.DateTimeField(null=True)
    tmdb_id = models.IntegerField(null=True)
    genre = models.ManyToManyField("Genre", related_name="movies", blank=True)
    role = models.CharField(max_length=128, blank=True)
    media_type = models.CharField(max_length=2, choices=MEDIA_TYPE_CHOICES, blank=True)
    poster_path = models.URLField(max_length=200, blank=True)
    credit_type = models.CharField(max_length=3, choices=CREDIT_TYPE_CHOICES, blank=True)

    def __str__(self):
        return self.title
    
    def get_genres(self):
        return ", ".join([x.name for x in self.genre.all()])

class Genre(models.Model):
    name = models.CharField(max_length=32)
    tmdb_id = models.IntegerField()
    

    def __str__(self):
        return self.name
    
    def get_movies(self):
        return ", ".join([x.title for x in self.movies.all()])
