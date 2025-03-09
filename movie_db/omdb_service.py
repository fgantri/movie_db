import requests
import json

class OMDbService:
    """Service for interacting with the OMDb API."""
    
    def __init__(self, api_key):
        """Initialize the OMDb API service with the API key.
        
        Args:
            api_key (str): The OMDb API key
        """
        self._api_key = api_key
        self._base_url = "http://www.omdbapi.com/"
        
    def search_movie_by_title(self, title):
        """Search for a movie by its title.
        
        Args:
            title (str): The movie title to search for
            
        Returns:
            dict: The movie data if found, None otherwise
        """
        params = {
            'apikey': self._api_key,
            't': title
        }
        
        try:
            response = requests.get(self._base_url, params=params)
            response.raise_for_status()  # Raise an exception for HTTP errors
            
            data = response.json()
            
            if data.get('Response') == 'True':
                return {
                    'title': data.get('Title', ''),
                    'year': int(data.get('Year', '0')) if data.get('Year', '').isdigit() else 0,
                    'rating': float(data.get('imdbRating', '0')) if data.get('imdbRating', '').replace('.', '').isdigit() else 0.0,
                    'poster': data.get('Poster', ''),
                    'plot': data.get('Plot', ''),
                    'director': data.get('Director', ''),
                    'actors': data.get('Actors', ''),
                    'genre': data.get('Genre', '')
                }
            return None
            
        except (requests.RequestException, json.JSONDecodeError, ValueError) as e:
            print(f"Error searching for movie: {str(e)}")
            return None
            
    def search_movies(self, search_term):
        """Search for movies matching a search term.
        
        Args:
            search_term (str): The search term to use
            
        Returns:
            list: A list of movie dictionaries that match the search term
        """
        params = {
            'apikey': self._api_key,
            's': search_term
        }
        
        try:
            response = requests.get(self._base_url, params=params)
            response.raise_for_status()
            
            data = response.json()
            
            if data.get('Response') == 'True' and 'Search' in data:
                results = []
                for movie in data['Search']:
                    # Fetch detailed info for each movie
                    movie_id = movie.get('imdbID')
                    if movie_id:
                        detailed_info = self.get_movie_by_id(movie_id)
                        if detailed_info:
                            results.append(detailed_info)
                return results
            return []
            
        except (requests.RequestException, json.JSONDecodeError) as e:
            print(f"Error searching for movies: {str(e)}")
            return []
    
    def get_movie_by_id(self, imdb_id):
        """Get detailed movie information by IMDb ID.
        
        Args:
            imdb_id (str): The IMDb ID of the movie
            
        Returns:
            dict: The movie data if found, None otherwise
        """
        params = {
            'apikey': self._api_key,
            'i': imdb_id
        }
        
        try:
            response = requests.get(self._base_url, params=params)
            response.raise_for_status()
            
            data = response.json()
            
            if data.get('Response') == 'True':
                return {
                    'title': data.get('Title', ''),
                    'year': int(data.get('Year', '0')) if data.get('Year', '').isdigit() else 0,
                    'rating': float(data.get('imdbRating', '0')) if data.get('imdbRating', '').replace('.', '').isdigit() else 0.0,
                    'poster': data.get('Poster', ''),
                    'plot': data.get('Plot', ''),
                    'director': data.get('Director', ''),
                    'actors': data.get('Actors', ''),
                    'genre': data.get('Genre', '')
                }
            return None
            
        except (requests.RequestException, json.JSONDecodeError) as e:
            print(f"Error getting movie by ID: {str(e)}")
            return None
