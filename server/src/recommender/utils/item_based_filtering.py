from dataclasses import dataclass
from typing import List

from recommender.models import Movie

from .movie_lens import MovieLens
from surprise import KNNBasic
from collections import defaultdict
from operator import itemgetter


@dataclass
class RecommendedData:
    movie: Movie
    rating: float


def findForUser(id: int):
    ml = MovieLens()
    data = ml.loadMovieLensLatestSmall()
    trainSet = data.build_full_trainset()

    model = KNNBasic(sim_options={"name": "cosine", "user_based": False})
    model.fit(trainSet)
    simsMatrix = model.compute_similarities()

    userIID = trainSet.to_inner_uid(id)

    # Get the top K items we rated
    userRatings = trainSet.ur[userIID]
    kNeighbors = []
    for rating in userRatings:
        if rating[1] > 4.0:
            kNeighbors.append(rating)

    # Get similar items to stuff we liked (weighted by rating)
    candidates = defaultdict(float)
    for itemID, rating in kNeighbors:
        similarityRow = simsMatrix[itemID]
        for innerID, score in enumerate(similarityRow):
            candidates[innerID] += score * (rating / 5.0)

    # Build a dictionary of stuff the user has already seen
    watched = {}
    for itemID, rating in trainSet.ur[userIID]:
        watched[itemID] = 1

    # Get top-rated items from similar users:
    recommendations: List[RecommendedData] = []
    pos = 0
    for itemID, ratingSum in sorted(
        candidates.items(), key=itemgetter(1), reverse=True
    ):
        if itemID not in watched:
            movieID = int(trainSet.to_raw_iid(itemID))
            movie = ml.getMovieInfo(movieID)
            if movie is None:
                continue

            recommendations.append(RecommendedData(movie, ratingSum))
            pos += 1
            if pos > 10:
                break

    return recommendations
