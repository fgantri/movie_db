import random
import statistics
import os

from movie_db import input_validator
from movie_db.output_formatter import call_with_vertical_margin
from movie_db.omdb_service import OMDbService


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

    def __init__(self, storage, omdb_api_key=None):
        """Initialize the MovieApp with a storage backend.
        
        Args:
            storage: An implementation of IStorage interface
            omdb_api_key: Optional API key for the OMDb API
        """
        self._storage = storage
        self._omdb_api_key = omdb_api_key
        self._omdb_service = None
        if omdb_api_key:
            self._omdb_service = OMDbService(omdb_api_key)
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
            "9": (self._command_generate_website, "Generate website"),
            "10": (self._command_sort_movies_by_year, "Movies sorted by year"),
            "11": (self._command_filter_movies, "Filter movies"),
            "12": (self._command_search_omdb, "Search movie on OMDb API")
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
                option = input("Enter choice (0-12): ")
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
        """Asks the user to enter a movie name and adds it to the database
        using data fetched from the OMDb API."""
        title = input_validator.get_input(prompt="Enter movie name: ",
                                          empty_msg="Movie name must not be empty.")
        
        # Initialize OMDb service if not done yet
        if not self._omdb_service:
            if not self._omdb_api_key:
                api_key = input_validator.get_input(
                    prompt="Please enter your OMDb API key: ",
                    empty_msg="API key must not be empty."
                )
                self._omdb_api_key = api_key
                self._omdb_service = OMDbService(api_key)
            else:
                self._omdb_service = OMDbService(self._omdb_api_key)
        
        try:
            print(f"Searching for '{title}' on OMDb API...")
            movie_data = self._omdb_service.search_movie_by_title(title)
            
            if not movie_data:
                print(f"No movie found with title '{title}'.")
                add_manually = input_validator.get_binary_input("Would you like to add the movie manually")
                
                if add_manually:
                    # Fall back to manual entry if movie not found
                    year = int(input_validator.get_number_input(prompt="Enter movie year: ",
                                                        error_msg="Please enter a valid year"))
                    rating = input_validator.get_number_input(prompt="Enter movie rating: ",
                                                          error_msg="Please enter a valid rating")
                    poster = input_validator.get_input(prompt="Enter movie poster URL (optional): ",
                                                   empty_msg="")
                    poster = poster if poster else "N/A"
                else:
                    return
            else:
                # Use the data from the API
                print("\nMovie found:")
                print(f"Title: {movie_data['title']}")
                print(f"Year: {movie_data['year']}")
                print(f"Rating: {movie_data['rating']}")
                
                # Confirm with user
                add_to_db = input_validator.get_binary_input("Do you want to add this movie to your database")
                if not add_to_db:
                    return
                
                title = movie_data['title']
                year = movie_data['year']
                rating = movie_data['rating']
                poster = movie_data['poster']
            
            if self._storage.add_movie(title, year, rating, poster):
                print(f"Movie '{title}' successfully added")
                # update movies cache
                self._refresh_movies_cache()
            else:
                print(f"Movie '{title}' already exists!")
                
        except Exception as e:
            print(f"Error fetching movie data: {str(e)}")
            print("Please check your internet connection or API key and try again.")
            print("Alternatively, try adding the movie manually.")
            add_manually = input_validator.get_binary_input("Would you like to add the movie manually")
            
            if add_manually:
                # Fall back to manual entry if there's an API error
                year = int(input_validator.get_number_input(prompt="Enter movie year: ",
                                                    error_msg="Please enter a valid year"))
                rating = input_validator.get_number_input(prompt="Enter movie rating: ",
                                                      error_msg="Please enter a valid rating")
                poster = input_validator.get_input(prompt="Enter movie poster URL (optional): ",
                                               empty_msg="")
                poster = poster if poster else "N/A"
                
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

    def _command_search_omdb(self):
        """Search for a movie using the OMDb API and add it to the database if found."""
        if not self._omdb_service:
            if not self._omdb_api_key:
                api_key = input_validator.get_input(
                    prompt="Please enter your OMDb API key: ",
                    empty_msg="API key must not be empty."
                )
                self._omdb_api_key = api_key
                self._omdb_service = OMDbService(api_key)
            else:
                self._omdb_service = OMDbService(self._omdb_api_key)
        
        search_term = input_validator.get_input(
            prompt="Enter movie title to search: ",
            empty_msg="Movie title must not be empty."
        )
        
        try:
            print(f"Searching for '{search_term}' on OMDb API...")
            movie_data = self._omdb_service.search_movie_by_title(search_term)
            
            if not movie_data:
                print(f"No movie found with title '{search_term}'.")
                return
            
            print("\nMovie found:")
            print(f"Title: {movie_data['title']}")
            print(f"Year: {movie_data['year']}")
            print(f"Rating: {movie_data['rating']}")
            print(f"Director: {movie_data['director']}")
            print(f"Actors: {movie_data['actors']}")
            print(f"Plot: {movie_data['plot']}")
            
            add_to_db = input_validator.get_binary_input("Do you want to add this movie to your database")
            
            if add_to_db:
                title = movie_data['title']
                year = movie_data['year']
                rating = movie_data['rating']
                poster = movie_data['poster']
                
                if self._storage.add_movie(title, year, rating, poster):
                    print(f"Movie '{title}' successfully added to your database")
                    # update movies cache
                    self._refresh_movies_cache()
                else:
                    print(f"Movie '{title}' already exists in your database!")
        except Exception as e:
            print(f"Error fetching movie data: {str(e)}")
            print("Please check your internet connection or API key and try again.")

    def _command_generate_website(self):
        """Generate a website to display all movies."""
        if not self._movies:
            print("No movies in the database. Add some movies first.")
            return
        
        try:
            # Define paths
            template_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'templates')
            template_file = os.path.join(template_dir, 'movie_template.html')
            css_file = os.path.join(template_dir, 'style.css')
            output_html = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'index.html')
            output_css = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'style.css')
            
            # Create templates directory if it doesn't exist
            if not os.path.exists(template_dir):
                os.makedirs(template_dir)
                print(f"Created templates directory: {template_dir}")

            # Check if template files exist
            template_html_exists = os.path.exists(template_file)
            template_css_exists = os.path.exists(css_file)

            # If template HTML doesn't exist, create a basic one
            if not template_html_exists:
                with open(template_file, 'w', encoding='utf-8') as f:
                    f.write("""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>${TITLE}</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <header>
        <h1>${TITLE}</h1>
    </header>
    <main class="movie-grid">
        ${MOVIE_GRID}
    </main>
    <footer>
        <p>Generated by Movie Database App</p>
    </footer>
</body>
</html>""")
                print(f"Created template HTML file: {template_file}")

            # If template CSS doesn't exist, create a basic one
            if not template_css_exists:
                with open(css_file, 'w', encoding='utf-8') as f:
                    f.write("""* {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}

body {
    font-family: Arial, sans-serif;
    line-height: 1.6;
    color: #333;
    background-color: #f4f4f4;
    padding: 20px;
}

header {
    background-color: #333;
    color: #fff;
    text-align: center;
    padding: 1rem;
    margin-bottom: 2rem;
}

footer {
    text-align: center;
    padding: 1rem;
    margin-top: 2rem;
    background-color: #333;
    color: #fff;
}

.movie-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
    gap: 2rem;
    padding: 1rem;
}

.movie-card {
    background: white;
    border-radius: 8px;
    overflow: hidden;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    transition: transform 0.3s ease;
}

.movie-card:hover {
    transform: translateY(-5px);
}

.movie-poster {
    width: 100%;
    height: 350px;
    object-fit: cover;
}

.movie-info {
    padding: 1rem;
}

.movie-title {
    font-size: 1.2rem;
    font-weight: bold;
    margin-bottom: 0.5rem;
}

.movie-details {
    font-size: 0.9rem;
    color: #666;
}

.movie-rating {
    margin-top: 0.5rem;
    display: inline-block;
    padding: 0.3rem 0.6rem;
    background-color: #f8d700;
    border-radius: 4px;
    font-weight: bold;
}""")
                print(f"Created template CSS file: {css_file}")

            # Read the template
            with open(template_file, 'r', encoding='utf-8') as f:
                template = f.read()
            
            # Generate movie grid HTML
            movie_grid_html = ""
            for movie in self._movies:
                poster_url = movie.get('poster', '')
                if not poster_url:
                    poster_url = "https://via.placeholder.com/300x450.png?text=No+Poster"
                
                movie_card = f"""
                <div class="movie-card">
                    <img src="{poster_url}" alt="{movie['title']} poster" class="movie-poster">
                    <div class="movie-info">
                        <div class="movie-title">{movie['title']}</div>
                        <div class="movie-details">{movie['year']}</div>
                        <div class="movie-rating">⭐ {movie['rating']}/10</div>
                    </div>
                </div>
                """
                movie_grid_html += movie_card
            
            # Replace placeholders in the template
            html_content = template.replace("${TITLE}", "My Movie Collection").replace("${MOVIE_GRID}", movie_grid_html)
            
            # Write the HTML file
            with open(output_html, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            # Copy the CSS file
            with open(css_file, 'r', encoding='utf-8') as src_file:
                css_content = src_file.read()
                with open(output_css, 'w', encoding='utf-8') as dest_file:
                    dest_file.write(css_content)
            
            print(f"Website generated successfully!")
            print(f"HTML file: {output_html}")
            print(f"CSS file: {output_css}")
            print("Open the HTML file in your web browser to view your movie collection.")
            
        except Exception as e:
            print(f"Error generating website: {str(e)}")
