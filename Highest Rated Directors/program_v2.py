import csv
from collections import defaultdict, namedtuple, Counter

NUM_TOP_DIRECTORS = 20
MOVIE_DATA = 'movie_metadata.csv'
Movie = namedtuple('Movie', 'title year score')


def get_movies_by_director():
    """ Extract data from <MOVIE-DATA> and create a dictionary with
    director: <Movie> key-value pairs. <Movie> must be after 1960 (inclusive).
    """
    directors = defaultdict(list)
    with open(MOVIE_DATA, encoding='utf-8') as f:
        dict_reader = csv.DictReader(f)
        for row in dict_reader:  # try - except might not catch cases where csv
            # key exists but has value None
            year = row.get('title_year')
            director = row.get('director_name')
            title = row.get('movie_title')
            score = row.get('imdb_score')
            if all([year, director, title, score]) and int(year) >= 1960:
                directors[director].append(
                    Movie(title=title, year=year,
                          score=score))
        return directors


def avg_score(movie_list):
    """Return the average imdb score of <Movie>s in <movie_list> rounded to one
    decimal point. """
    return round(
        sum(float(m.score) for m in movie_list) / len(movie_list), 1)


def top_directors_with_at_least_four():
    """Return the top 20 directors with at least four movies, based on average
    score of movies """
    director_dictionary = get_movies_by_director()

    at_least_four = {(director, avg_score(movie_list)): movie_list for
                     director, movie_list in
                     director_dictionary.items() if len(movie_list) >= 4}

    return sorted(at_least_four.items(), key=lambda x: x[0][1], reverse=True)[
           :NUM_TOP_DIRECTORS]


def print_results():
    fmt_directory_entry = "{counter:0>2}. {director:<52} {avg}"
    divider = '-' * 60
    fmt_movie_entry = "{year}] {title:<50} {score}"

    for counter, director_info in enumerate(top_directors_with_at_least_four(),
                                            1):
        print()
        director, rating = director_info[0]
        print(fmt_directory_entry.format(counter=counter, director=director,
                                         avg=rating))
        print(divider)
        for movie in sorted(director_info[1], key=lambda m: m.score,
                            reverse=True):
            if len(movie.title) <= 45:
                print(fmt_movie_entry.format(year=movie.year, title=movie.title,
                                             score=movie.score))
            else:
                print(f"{movie.year}] {movie.title[:45]}-".ljust(
                    57) + f"{movie.score}" + f"\n{movie.title[45:]}")


if __name__ == '__main__':
    print_results()
