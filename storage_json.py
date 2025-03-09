import json
import os

from istorage import IStorage


class StorageJson(IStorage):
    def __init__(self, file_path):
        self._file_path = file_path
        # Create the file if it doesn't exist
        if not os.path.exists(self._file_path):
            with open(self._file_path, "w") as f:
                f.write(json.dumps([]))

    def list_movies(self):
        """Returns a list of dictionaries that
        contains the movies information in the database.

        The function loads the information from the JSON
        file and returns the data.
        """
        try:
            with open(self._file_path, "r") as f:
                return json.loads(f.read())
        except (FileNotFoundError, json.JSONDecodeError):
            # Create the file if it doesn't exist or if JSON is invalid
            with open(self._file_path, "w") as f:
                f.write(json.dumps([]))
            return []

    def add_movie(self, title, year, rating, poster):
        """Adds a movie to the movie's database.

        Loads the information from the JSON file, add the movie,
        and saves it.
        """
        movie_list = self.list_movies()

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
            f.write(json.dumps(movie_list, indent=2))  # Added indentation for readability
        return True

    def delete_movie(self, title):
        """Deletes a movie from the movie's storage.

        Loads the information from the JSON file, deletes the movie,
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
                f.write(json.dumps(movie_list, indent=2))  # Added indentation for readability
            return True
        return False

    def update_movie(self, title, rating):
        """Updates a movie from the storage.

        Loads the information from the JSON file, updates the movie,
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
                f.write(json.dumps(movie_list, indent=2))  # Added indentation for readability
            return True
        return False


def main():
    """Test main for json storage"""
    movie_library = StorageJson('movies.json')
    print(movie_library.list_movies())
    # Assuming you have a class instance named `movie_library` with the `add_movie` method:
    movie_library.add_movie("Inception", 2010, 8.8, "https://example.com/inception.jpg")
    movie_library.add_movie("The Dark Knight", 2008, 9.0, "https://example.com/dark_knight.jpg")
    movie_library.add_movie("Pulp Fiction", 1994, 8.9, "https://example.com/pulp_fiction.jpg")
    movie_library.add_movie("The Godfather", 1972, 9.2, "https://example.com/godfather.jpg")
    movie_library.add_movie("The Matrix", 1999, 8.7, "https://example.com/matrix.jpg")
    movie_library.add_movie("Fight Club", 1999, 8.8, "https://example.com/fight_club.jpg")
    movie_library.add_movie("Forrest Gump", 1994, 8.8, "https://example.com/forrest_gump.jpg")
    movie_library.add_movie("Interstellar", 2014, 8.6, "https://example.com/interstellar.jpg")
    movie_library.add_movie("The Lord of the Rings: The Return of the King", 2003, 9.0,
                            "https://example.com/lotr_return.jpg")
    print(movie_library.list_movies())
    movie_library.delete_movie("Pulp Fiction")
    movie_library.update_movie("The Dark Knight", 10)
    movie_library.delete_movie("The Godfather")
    print(movie_library.list_movies())


if __name__ == "__main__":
    main()
