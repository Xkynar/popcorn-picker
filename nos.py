import requests

class NOSClient:
    """Client to interact with NOS Cinemas API"""
    def __init__(self):
        self.base_url = "https://www.cinemas.nos.pt/graphql/execute.json/cinemas"
        pass

    def get_movie_catalog(self):
        url = f"{self.base_url}/getAllMovies"
        response = requests.get(url)
        allMovies = response.json()["data"]["movieList"]["items"]
        catalog = filter(lambda m: m["intheaters"] == True, allMovies)
        return catalog
