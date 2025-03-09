import random
import statistics

import input_validator
from output_formatter import call_with_vertical_margin


def exit_app():
    """Exits the app"""
    print("Bye!")
    exit(0)


def print_movies(movies):
    """Print all the given movies, along with their rating and year of release."""
    if not movies:
        print("No movies found.")
        return
        
    for movie in movies:
        print(f"{movie['title']} ({movie['year']}): {movie['rating']}")


class MovieApp:
    """Movie database application that provides various operations on a movie collection."""

    def __init__(self, storage):
        """Initialize the MovieApp with a storage backend.
        
        Args:
            storage: An implementation of IStorage interface
        """
        self._storage = storage
        # Initialize movies cache
        self._refresh_movies_cache()
        self._menu = {
            "0": (exit_app, "Exit"),
            "1": (self._command_list_movies, "List movies"),
            "2": (self._command_add_movie, "Add movie"),
            "3": (self._command_delete_movie, "Delete movie"),
            "4": (self._command_update_movie, "Update movie"),
            "5": (self._command_print_movies_stats, "Stats"),
            "6": (self._command_print_random_movie, "Random movie"),
            "7": (self._command_search_movies, "Search movie"),
            "8": (self._command_sort_movies_by_rating, "Movies sorted by rating"),
            "9": (self._command_sort_movies_by_year, "Movies sorted by year"),
            "10": (self._command_filter_movies, "Filter movies")
        }

    def _refresh_movies_cache(self):
        """Refresh the movies cache from storage."""
        self._movies = self._storage.list_movies()

    def run(self):
        """Runs the app menu and asks user to pick a task until quit"""
        print("********** My Movies Database **********")
        while True:
            call_with_vertical_margin(self._print_menu)
            try:
                option = input("Enter choice (0-10): ")
                cmd = self._menu[option][0]
            except KeyError:
                print("Invalid choice")
                continue
            except Exception as e:
                print(f"An error occurred: {str(e)}")
                continue
                
            try:
                call_with_vertical_margin(cmd)
            except Exception as e:
                print(f"An error occurred: {str(e)}")
                
            input("Press enter to continue ")

    def _command_list_movies(self):
        """Print all the movies, along with their rating and year of release.
        In addition, the command prints how many movies there are in total in the database."""
        print(f"{len(self._movies)} movies in total")
        print_movies(self._movies)

    def _command_add_movie(self):
        """Asks the user to enter a movie name, a rating, a year and adds it to the database"""
        title = input_validator.get_input(prompt="Enter new movie name: ",
                                          empty_msg="Movie name must not be empty.")
        # returns float input but needing int
        year = int(input_validator.get_number_input(prompt="Enter new movie year: ",
                                                    error_msg="Please enter a valid year"))
        rating = input_validator.get_number_input(prompt="Enter new movie rating: ",
                                                  error_msg="Please enter a valid rating")
        poster = input_validator.get_input(prompt="Enter new movie poster: ",
                                           empty_msg="Movie poster must not be empty.")
        if self._storage.add_movie(title, year, rating, poster):
            print(f"Movie '{title}' successfully added")
            # update movies cache
            self._refresh_movies_cache()
        else:
            print(f"Movie '{title}' already exists!")

    def _command_delete_movie(self):
        """Asks the user to enter a movie name, and delete it.
        If the movie doesn't exist in the database, print an error message"""
        title = input_validator.get_input(prompt="Enter movie name to delete: ",
                          empty_msg="Movie name must not be empty.")
        if self._storage.delete_movie(title):
            print(f"Movie '{title}' successfully deleted")
            # update movies cache
            self._refresh_movies_cache()
        else:
            print(f"Movie '{title}' doesn't exist!")

    def _command_update_movie(self):
        """Asks the user to enter a movie name, and then check if it exists.
        If the movie doesn't print an error message.
        If it exists, ask the user to enter a new rating, and update the movie's rating in the database."""
        title = input_validator.get_input(prompt="Enter movie name to update: ",
                          empty_msg="Movie name must not be empty.")
        rating = input_validator.get_number_input(prompt="Enter new movie rating: ",
                                  error_msg="Please enter a valid rating")
        if self._storage.update_movie(title, rating):
            print(f"Movie '{title}' successfully updated")
            # update movies cache
            self._refresh_movies_cache()
        else:
            print(f"Movie '{title}' doesn't exist!")

    def _command_print_movies_stats(self):
        """Print statistics about the movies in the database"""
        if not self._movies:
            print("No movies in the database. Add some movies first.")
            return
            
        ratings = [m["rating"] for m in self._movies]

        average_rating = round(statistics.mean(ratings), 2)
        median_rating = round(statistics.median(ratings), 2)
        best_movie = max(self._movies, key=lambda m: m["rating"])
        worst_movie = min(self._movies, key=lambda m: m["rating"])

        print(f"Average rating: {average_rating}")
        print(f"Median rating: {median_rating}")
        print(f"Best movie: {best_movie['title']}, {best_movie['rating']}")
        print(f"Worst movie: {worst_movie['title']}, {worst_movie['rating']}")

    def _command_print_random_movie(self):
        """Print a random movie and it's rating."""
        if not self._movies:
            print("No movies in the database. Add some movies first.")
            return
            
        random_movie = random.choice(self._movies)
        print(f"Your movie for tonight: {random_movie['title']}, it's rated {random_movie['rating']}")

    def _command_search_movies(self):
        """Asks the user to enter a part of a movie name, and then search all the movies
        and prints all the movies that matched the user's query, along with the rating."""
        search_query = input("Enter part of movie name: ").strip().lower()
        matching_movies = []
        
        for movie in self._movies:
            if search_query in movie["title"].lower():
                matching_movies.append(movie)
                
        if matching_movies:
            print(f"Found {len(matching_movies)} matching movies:")
            print_movies(matching_movies)
        else:
            print(f"No movies found matching '{search_query}'")

    def _command_sort_movies_by_rating(self):
        """Print all the movies and their ratings, in descending or ascending order by the rating.
        Put differently, the best movie should be printed first, and the worst movie should be printed last.
        (vice versa)"""
        if not self._movies:
            print("No movies in the database. Add some movies first.")
            return
            
        is_descending_order = input_validator.get_binary_input("Do you want the high rated movies first")
        movies = sorted(self._movies, key=lambda m: m["rating"], reverse=is_descending_order)
        order_text = "descending" if is_descending_order else "ascending"
        print(f"Movies sorted by rating ({order_text}):")
        print_movies(movies)

    def _command_sort_movies_by_year(self):
        """Print all the movies and their ratings, in descending or ascending order by the year.
        Put differently, the newest movie should be printed first, and the worst oldest should be printed last.
        (vice versa)"""
        if not self._movies:
            print("No movies in the database. Add some movies first.")
            return
            
        is_descending_order = input_validator.get_binary_input("Do you want the latest movies first")
        movies = sorted(self._movies, key=lambda m: m["year"], reverse=is_descending_order)
        order_text = "newest first" if is_descending_order else "oldest first"
        print(f"Movies sorted by year ({order_text}):")
        print_movies(movies)

    def _command_filter_movies(self):
        """Filters a list of movies based on specific criteria given from user input
        such as minimum rating, start year, and end year."""
        if not self._movies:
            print("No movies in the database. Add some movies first.")
            return
            
        min_rating = input_validator.get_optional_input(prompt="Enter minimum rating",
                                        cast_func=float,
                                        error_msg="Invalid input. Please enter a valid rating.")
        start_year = input_validator.get_optional_input(prompt="Enter start year",
                                        cast_func=int,
                                        error_msg="Invalid input. Please enter a valid start year.")
        end_year = input_validator.get_optional_input(prompt="Enter end year",
                                      cast_func=int,
                                      error_msg="Invalid input. Please enter a valid end year.")
                                      
        filtered_movies = []
        for movie in self._movies:
            valid_min_rating = min_rating is None or movie["rating"] >= min_rating
            valid_start_year = start_year is None or movie["year"] >= start_year
            valid_end_year = end_year is None or movie["year"] <= end_year
            if valid_min_rating and valid_start_year and valid_end_year:
                filtered_movies.append(movie)
                
        filter_criteria = []
        if min_rating is not None:
            filter_criteria.append(f"rating >= {min_rating}")
        if start_year is not None:
            filter_criteria.append(f"year >= {start_year}")
        if end_year is not None:
            filter_criteria.append(f"year <= {end_year}")
            
        criteria_text = " and ".join(filter_criteria) if filter_criteria else "no filters"
        print(f"Filtered Movies ({criteria_text}):")
        print_movies(filtered_movies)

    def _print_menu(self):
        """Prints a menu of available operations"""
        print("Menu:")
        for opt_key, option in self._menu.items():
            _, opt_description = option
            print(f"{opt_key}. {opt_description}")
