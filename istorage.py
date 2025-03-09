from abc import ABC, abstractmethod


class IStorage(ABC):

    @abstractmethod
    def list_movies(self):
        """Returns a list of dictionaries that
        contains the movies information in the database."""
        pass

    @abstractmethod
    def add_movie(self, title, year, rating, poster):
        """Adds a movie to the movie's database."""
        pass

    @abstractmethod
    def delete_movie(self, title):
        """Deletes a movie from the movie's storage."""
        pass

    @abstractmethod
    def update_movie(self, title, rating):
        """Updates a movie from the storage."""
        pass
