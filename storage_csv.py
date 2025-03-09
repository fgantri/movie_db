from istorage import IStorage
import os


def movies_to_csv(movies, separator):
    csv_string = separator.join(["title", "year", "rating", "poster"]) + "\n"
    for movie in movies:
        row = [movie['title'], movie["year"], movie["rating"], movie["poster"]]
        row = [str(col) for col in row]
        csv_string += separator.join(row) + "\n"
    return csv_string


class StorageCsv(IStorage):

    def __init__(self, file_path, separator):
        self._file_path = file_path
        self._separator = separator
        # Create the file if it doesn't exist
        if not os.path.exists(self._file_path):
            with open(self._file_path, "w") as f:
                f.write(movies_to_csv([], self._separator))

    def list_movies(self):
        """Returns a list of dictionaries that
        contains the movies information in the database.

        The function loads the information from the CSV
        file and returns the data.
        """
        movies = []
        try:
            with open(self._file_path, "r") as f:
                lines = f.readlines()
                if len(lines) > 1:  # Check if there's content beyond the header
                    for line in lines[1:]:
                        line = line.strip()
                        if not line:  # Skip empty lines
                            continue
                        row = line.split(self._separator)
                        if len(row) != 4:
                            continue
                        title, year, rating, poster = row

                        try:
                            movies.append({
                                "title": title,
                                "year": int(year),
                                "rating": float(rating),
                                "poster": poster
                            })
                        except (ValueError, TypeError):
                            # Skip entries with invalid data
                            continue
        except FileNotFoundError:
            # Create the file if it doesn't exist
            with open(self._file_path, "w") as f:
                f.write(movies_to_csv([], self._separator))
        
        return movies

    def add_movie(self, title, year, rating, poster):
        """Adds a movie to the movie's database.

        Loads the information from the CSV file, add the movie,
        and saves it.
        """
        movie_list = self.list_movies()
        # check if movie exists
        for movie in movie_list:
            if title.lower() == movie["title"].lower():  # Case-insensitive comparison
                return False

        movie_list.append({
            "title": title,
            "year": year,
            "rating": rating,
            "poster": poster
        })

        with open(self._file_path, "w") as f:
            f.write(movies_to_csv(movie_list, self._separator))
        return True

    def delete_movie(self, title):
        """Deletes a movie from the movie's storage.

        Loads the information from the CSV file, deletes the movie,
        and saves it.
        """
        movie_list = self.list_movies()

        del_index = None
        for i, movie in enumerate(movie_list):
            if movie["title"].lower() == title.lower():  # Case-insensitive comparison
                del_index = i
                break

        if del_index is not None:
            del movie_list[del_index]

            with open(self._file_path, "w") as f:
                f.write(movies_to_csv(movie_list, self._separator))
            return True
        return False

    def update_movie(self, title, rating):
        """Updates a movie from the storage.

        Loads the information from the CSV file, updates the movie,
        and saves it.
        """
        movie_list = self.list_movies()

        update_index = None
        for i in range(len(movie_list)):
            if movie_list[i]["title"].lower() == title.lower():  # Case-insensitive comparison
                update_index = i
                break

        if update_index is not None:
            movie_list[update_index]["rating"] = rating

            with open(self._file_path, "w") as f:
                f.write(movies_to_csv(movie_list, self._separator))
            return True
        return False
