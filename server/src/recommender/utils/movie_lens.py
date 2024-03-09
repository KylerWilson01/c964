import re

from collections import defaultdict
from typing import Any, Dict, List, Optional

from surprise.dataset import Dataset, DatasetAutoFolds
from surprise.reader import Reader
from recommender.models import Movie, Rating
from pandas import DataFrame


class MovieLens:
    def loadMovieLensLatestSmall(self) -> DatasetAutoFolds:
        ratingQuerySet = Rating.objects.all()
        ratingDataframe = DataFrame.from_records(
            ratingQuerySet.values(),
            columns=["userId", "movie_id", "rating"],
        )

        data = Dataset.load_from_df(
            ratingDataframe,
            reader=Reader(line_format="user item rating", rating_scale=(1, 5)),
        )

        return data

    def getUserRatings(self, userId: int) -> List[Rating]:
        return list(Rating.objects.filter(userId=userId))

    def getPopularityRanks(self) -> Dict[int, int]:
        ratings: Dict[int, int] = defaultdict(int)
        rankings: Dict[int, int] = defaultdict(int)

        allRatings = Rating.objects.all()
        for rating in allRatings:
            movie = rating.get_movie()
            if movie is not None:
                ratings[movie.movieId] += 1

        rank = 1
        for movieID, _ in sorted(ratings.items(), key=lambda x: x[1], reverse=True):
            rankings[movieID] = rank
            rank += 1

        return rankings

    def getGenres(self) -> Dict[int, Any]:
        genres = defaultdict(list)
        genreIDs: Dict[str, int] = {}
        maxGenreID = 0

        movies = list(Movie.objects.all())

        for movie in movies:
            movieGenres = movie.genres.split("|")
            genreIDList = []

            for genre in movieGenres:
                if genre in genreIDs:
                    genreID = genreIDs[genre]
                else:
                    genreID = maxGenreID
                    genreIDs[genre] = genreID
                    maxGenreID += 1
                genreIDList.append(genreID)
            genres[movie.movieId] = genreIDList

        # Convert integer-encoded genre lists to bitfields that we can treat as vectors
        for movieID, genreIDList in genres.items():
            bitfield = [0] * maxGenreID
            for genreID in genreIDList:
                bitfield[genreID] = 1
            genres[movieID] = bitfield

        return genres

    def getYears(self) -> Dict[int, int]:
        p = re.compile(r"(?:\((\d{4})\))?\s*$")
        years = defaultdict(int)

        movieReader = Movie.objects.all()
        for row in movieReader:
            m = p.search(row.title)
            if m is not None:
                year = m.group(1)
                if year:
                    years[row.movieId] = int(year)

        return years

    def getMovieName(self, movieID: int) -> Optional[str]:
        return Movie.objects.get(movieId=movieID).title

    def getMovieInfo(self, movieID: int) -> Optional[Movie]:
        return Movie.objects.get(movieId=movieID)

    def getMovieID(self, movieName: str) -> Optional[int]:
        return Movie.objects.get(title=movieName).movieId
