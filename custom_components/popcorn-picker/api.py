"""API clients to access movie data."""

from typing import Any, Dict, List, Optional
import uuid

import aiohttp
import requests

from .types import Movie, MovieRating


class _NOSCinemasClient:
    """Client to interact with NOS Cinemas API."""

    def __init__(self) -> None:
        """Initialize the NOS Cinemas client."""
        self.base_url = "https://www.cinemas.nos.pt/graphql/execute.json/cinemas"

    async def get_movie_catalog(self) -> list[Movie]:
        """Fetch the movie catalog asynchronously."""
        url = f"{self.base_url}/getAllMovies"
        async with aiohttp.ClientSession() as session, session.get(url) as response:
            response.raise_for_status()  # Raise for HTTP errors
            allMovies_data = await response.json()
            allMovies_data = allMovies_data["data"]["movieList"]["items"]
            catalog_data = filter(lambda m: m["intheaters"], allMovies_data)
            return [Movie(**movie) for movie in catalog_data]


class MovieAPI:
    """Client to orchestrate the APIs."""

    def __init__(self, param1) -> None:
        """Initialize the orchestration client."""
        self.param1 = param1
        self.cinema_client = _NOSCinemasClient()
        self.rt_client = _RottenTomatoesClient()

    async def fetch_movies(self) -> list[Movie]:
        """Fetch the latest catalog."""
        movies = await self.cinema_client.get_movie_catalog()
        return movies[:2]

    async def fetch_movie_details(self, title, year) -> MovieRating:
        """Fetch details from a movie."""
        return await self.rt_client.get_movie_ratings(title, year)


class _RottenTomatoesClient:
    """Client to interact with the Rotten Tomatoes API."""

    def __init__(self) -> None:
        """Initialize the Rotten Tomatoes client."""
        self.base_url = "https://79frdp12pn-dsn.algolia.net/1/indexes/*"
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "x-algolia-usertoken": str(uuid.uuid4()),
            "x-algolia-agent": "Algolia for JavaScript (4.14.3); Browser (lite)",
            "x-algolia-api-key": "175588f6e5f8319b27702e4cc4013561",
            "x-algolia-application-id": "79FRDP12PN",
        }

    async def get_movie_ratings(self, name: str, year: int) -> MovieRating | None:
        """Fetch movie ratings from Rotten Tomatoes by name and year asynchronously."""
        try:
            data = await self._query_api(name)
            hits = self._extract_hits(data)
            movie = self._find_matching_movie(hits, name, year)

            return self._format_movie_ratings(movie) if movie else None
        except Exception as e:
            raise RuntimeError(f"[RT API] Error retrieving movie ratings: {e}")

    async def _query_api(self, name: str) -> Dict[str, Any]:
        """Send an asynchronous request to the Rotten Tomatoes API."""
        async with (
            aiohttp.ClientSession() as session,
            session.post(
                f"{self.base_url}/queries",
                json={
                    "requests": [
                        {
                            "indexName": "content_rt",
                            "query": name,
                            "params": "filters=isEmsSearchable=1&hitsPerPage=20",
                        }
                    ]
                },
                headers=self.headers,
            ) as response,
        ):
            response.raise_for_status()
            return await response.json()

    @staticmethod
    def _extract_hits(data: dict[str, Any]) -> list[dict[str, Any]]:
        """Extract movie hits from API response."""
        return next(
            (
                result.get("hits", [])
                for result in data.get("results", [])
                if result.get("index") == "content_rt"
            ),
            [],
        )

    @staticmethod
    def _find_matching_movie(
        hits: list[dict[str, Any]], name: str, year: int
    ) -> dict[str, Any] | None:
        """Find a movie in the hits list that matches the given name and year."""
        for movie in hits:
            if movie.get("releaseYear") == year and (
                movie.get("title") == name or name in movie.get("title", "")
            ):
                return movie
        return None

    @staticmethod
    def _format_movie_ratings(movie: dict[str, Any]) -> MovieRating:
        """Format movie ratings into a structured dictionary."""
        rotten_tomatoes = movie.get("rottenTomatoes", {})
        return MovieRating(
            url=f"https://www.rottentomatoes.com/m/{movie.get('vanity')}",
            audiencerating=_RottenTomatoesClient._get_audience_rating(
                rotten_tomatoes.get("audienceScore", 0)
            ),
            audiencescore=rotten_tomatoes.get("audienceScore"),
            criticsrating=_RottenTomatoesClient._get_critics_rating(
                rotten_tomatoes.get("criticsScore", 0),
                rotten_tomatoes.get("certifiedFresh", False),
            ),
            criticsscore=rotten_tomatoes.get("criticsScore"),
        )

    @staticmethod
    def _get_critics_rating(score: int, certified_fresh: bool) -> str:
        """Get the critics rating based on score and certification."""
        if certified_fresh:
            return "Certified Fresh"
        return "Fresh" if score >= 60 else "Rotten"

    @staticmethod
    def _get_audience_rating(score: int) -> str:
        """Get the audience rating based on the score."""
        return "Upright" if score >= 60 else "Spilled"
