import csv
from collections import defaultdict, namedtuple, Counter
from my_library import fill_string

MOVIE_DATA = 'movie_metadata.csv'
Movie = namedtuple('Movie', 'title year score')


def get_movies_by_director():
    """ Extract data from <MOVIE-DATA> and create a dictionary with
    director: <Movie> key-value pairs. <Movie> must be after 1960 (inclusive).
    """
    with open(MOVIE_DATA, encoding='utf-8') as f:
        dict_reader = csv.DictReader(f)
        director_dictionary = defaultdict(list)
        for row in dict_reader:
            year = row.get('title_year')
            director = row.get('director_name')
            title = row.get('movie_title')
            score = row.get('imdb_score')
            if all([year, director, title, score]) and int(year) >= 1960:
                director_dictionary[director].append(
                    Movie(title=title, year=year,
                          score=score))
        return director_dictionary


def avg_score(movie_list):
    """Return the average imdb score of <Movie>s in <movie_list> rounded to one
    decimal point. """
    return round(
        sum(float(Movie.score) for Movie in movie_list) / len(movie_list), 1)


def top_20_with_at_least_four():
    """Return the top 20 directors with at least four movies, based on average
    score of movies """
    director_dictionary = get_movies_by_director()

    at_least_four = [director for director, movie_list in
                     director_dictionary.items() if len(movie_list) >= 4]

    score_directory = {director: avg_score(director_dictionary[director]) for
                       director in at_least_four}

    return Counter(score_directory).most_common(20)


def main():
    director_dictionary = get_movies_by_director()
    counter1 = 1
    for item in top_20_with_at_least_four():
        director = item[0]
        score = item[1]
        movie_list = director_dictionary[director]
        counter1_repr = f"0{counter1}" if counter1 < 10 else counter1
        header = f"{counter1_repr}. {director}".ljust(60) + f"{score}"
        divider = "-" * len(header)
        print(header)
        print(divider)
        for Movie in sorted(movie_list, key=lambda Movie: Movie.score,
                            reverse=True):
            title = fill_string(Movie.title.strip(), 40)
            hyphenated_title = title[:40] + '-' + title[40:] if len(title) > 40 \
                else title  # hyphenated case assumes two lines (80 char) max
            print(
                f"{Movie.year}] {hyphenated_title[:41]}".ljust(
                    60) + f"{Movie.score}" + hyphenated_title[
                                             41:42] + '      ' + hyphenated_title[
                                                                 42:])
        print()
        counter1 += 1


if __name__ == '__main__':
    main()
