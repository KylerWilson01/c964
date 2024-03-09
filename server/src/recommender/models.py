from typing import Optional
from django.db import models


# Create your models here.
class Movie(models.Model):
    movieId = models.AutoField(primary_key=True)
    title = models.CharField()
    genres = models.TextField()


class Link(models.Model):
    movieId = models.OneToOneField(Movie, on_delete=models.CASCADE, primary_key=True)
    imdbId = models.IntegerField(null=True)
    tmdbId = models.IntegerField(null=True)


class Rating(models.Model):
    id = models.AutoField(primary_key=True)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    userId = models.IntegerField()
    rating = models.DecimalField(max_digits=5, decimal_places=2)
    timestamp = models.BigIntegerField()

    def get_movie(self) -> Optional[Movie]:
        return self.movie


class Tag(models.Model):
    id = models.AutoField(primary_key=True)
    userId = models.IntegerField()
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    tag = models.TextField()
    timestamp = models.BigIntegerField()
