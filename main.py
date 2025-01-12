from nos import NOSClient
from rottentomatoes import RTClient
from datetime import datetime
from tabulate import tabulate

if __name__ == "__main__":
    cinemaClient = NOSClient()
    rtClient = RTClient()

    try:
        catalog = cinemaClient.get_movie_catalog()
        # Remove duplicates by using a set of (originaltitle, releasedate) tuples
        unique_movies = list({(movie["originaltitle"], movie["releasedate"]) for movie in catalog})

        # Convert back to a list of dictionaries with unique title/date pairs
        catalog = [{"originaltitle": title, "releasedate": date} for title, date in unique_movies]

        results = []
        for movie in catalog:
            movie_name = movie["originaltitle"]
            movie_date = datetime.strptime(movie["releasedate"], "%Y-%m-%dT%H:%M")
            rating = rtClient.get_movie_ratings(movie_name, movie_date.year)
            results.append(rating)

        results = sorted(results, key=lambda m: m["criticsScore"], reverse=True)

        print(tabulate(results, headers="keys", tablefmt="pretty"))
    except Exception as e:
        print(f"Error: {e}")
