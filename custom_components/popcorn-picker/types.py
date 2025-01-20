"""The Popcorn Picker data types."""

from pydantic import BaseModel


class Movie(BaseModel):
    """Data structure for a movie."""

    uuid: str
    title: str
    originaltitle: str
    classification: str
    genre: str
    releasedate: str


class MovieRating(BaseModel):
    """Data structure for a movie rating."""

    criticsrating: str
    criticsscore: int
    audiencerating: str
    audiencescore: int
    url: str
