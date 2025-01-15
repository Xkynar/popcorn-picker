import requests
import uuid
from typing import Optional, Dict


class RTClient:
    """
    Client to interact with the Rotten Tomatoes API
    Inspired by https://github.com/sct/overseerr/blob/develop/server/api/rating/rottentomatoes.ts
    """

    def __init__(self):
        self.base_url = "https://79frdp12pn-dsn.algolia.net/1/indexes/*"
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "x-algolia-usertoken": str(uuid.uuid4()),
            "x-algolia-agent": "Algolia%20for%20JavaScript%20(4.14.3)%3B%20Browser%20(lite)",
            "x-algolia-api-key": "175588f6e5f8319b27702e4cc4013561",
            "x-algolia-application-id": "79FRDP12PN",
        }

    def get_movie_ratings(self, name: str, year: int) -> Optional[Dict[str, any]]:
        try:
            # Send request to Algolia API
            response = requests.post(
                f"{self.base_url}/queries",
                json={
                    "requests": [
                        {
                            "indexName": "content_rt",
                            "query": name,
                            "params": "filters=isEmsSearchable%20%3D%201&hitsPerPage=20",
                        }
                    ]
                },
                headers=self.headers,
            )
            data = response.json()

            # Find results for content_rt
            content_results = next(
                (r for r in data.get("results", []) if r["index"] == "content_rt"), None
            )

            if not content_results:
                return None

            # Try to find a matching movie by name and year
            movie = self._find_matching_movie(content_results["hits"], name, year)

            if not movie:
                return None

            # Return the movie ratings in the specified format
            return {
                "title": movie["title"],
                "url": f"https://www.rottentomatoes.com/m/{movie['vanity']}",
                "criticsRating": self._get_critics_rating(
                    movie["rottenTomatoes"]["criticsScore"],
                    movie["rottenTomatoes"]["certifiedFresh"],
                ),
                "criticsScore": movie["rottenTomatoes"]["criticsScore"],
                "audienceRating": self._get_audience_rating(
                    movie["rottenTomatoes"]["audienceScore"]
                ),
                "audienceScore": movie["rottenTomatoes"]["audienceScore"],
                "year": int(movie["releaseYear"]),
            }

        except Exception as e:
            raise RuntimeError(f"[RT API] Failed to retrieve movie ratings: {str(e)}")

    def _find_matching_movie(self, hits, name, year):
        # Try various strategies to find a matching movie
        for strategy in [
            lambda: next(
                (
                    movie
                    for movie in hits
                    if movie["releaseYear"] == year and movie["title"] == name
                ),
                None,
            ),
            lambda: next(
                (
                    movie
                    for movie in hits
                    if movie["releaseYear"] == year and name in movie["title"]
                ),
                None,
            ),
            lambda: next(
                (movie for movie in hits if movie["releaseYear"] == year), None
            ),
            lambda: next((movie for movie in hits if movie["title"] == name), None),
        ]:
            movie = strategy()
            if movie:
                return movie
        return None

    def _get_critics_rating(self, score: int, certified_fresh: bool) -> str:
        if certified_fresh:
            return "Certified Fresh"
        elif score >= 60:
            return "Fresh"
        else:
            return "Rotten"

    def _get_audience_rating(self, score: int) -> str:
        return "Upright" if score >= 60 else "Spilled"
