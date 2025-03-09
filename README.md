# Movie Database Application

A professional command-line application for managing a collection of movies, with support for multiple storage backends (CSV and JSON) and OMDb API integration.

## Features

- List all movies in the database
- Add new movies using the OMDb API (just enter the title!)
- Delete movies by title
- Update movie ratings
- View movie statistics (average rating, median rating, best and worst movies)
- Get random movie recommendations
- Search for movies by title
- Sort movies by rating or year
- Filter movies by rating, start year, and end year
- Generate a website to showcase your movie collection
- Search movies on OMDb API and add them to your database

## Installation

1. Clone the repository:
```
git clone <repository-url>
cd movie_db
```

2. Install dependencies:
```
pip install -r requirements.txt
```

3. Create a `.env` file in the project root with your OMDb API key:
```
OMDB_API_KEY=your_api_key_here
```

## Usage

```
python main.py [storage_type] [omdb_api_key]
```

Where:
- `storage_type` is optional and can be one of:
  - `csv` - Use CSV file storage (default)
  - `json` - Use JSON file storage
- `omdb_api_key` is optional if you've set it in the `.env` file

Example:
```
python main.py json 1a2b3c4d
```

## Project Structure

```
movie_db/
├── data/               # Data storage directory
│   ├── movies.csv      # CSV storage file
│   └── movies.json     # JSON storage file
├── movie_db/           # Main package
│   ├── __init__.py     # Package initialization
│   ├── movie_app.py    # Main application logic
│   ├── input_validator.py # Input validation utilities
│   ├── output_formatter.py # Output formatting utilities
│   ├── omdb_service.py # Service for OMDb API integration
│   └── storage/        # Storage package
│       ├── __init__.py # Package initialization
│       ├── istorage.py # Storage interface
│       ├── storage_csv.py # CSV storage implementation
│       └── storage_json.py # JSON storage implementation
├── templates/         # Website templates
│   ├── movie_template.html # HTML template for movie website
│   └── style.css      # CSS for website styling
├── .env              # Environment variables (API keys)
├── .gitignore        # Git ignore file
├── main.py           # Application entry point
├── README.md         # Project documentation
└── requirements.txt  # Project dependencies
```

## Data Storage

The application supports two storage backends:

1. **CSV Storage**: Stores data in a comma-separated values file (`data/movies.csv`)
2. **JSON Storage**: Stores data in a JSON file (`data/movies.json`)

The storage files are created automatically if they don't exist.

## OMDb API Integration

The application integrates with the [OMDb API](https://www.omdbapi.com/) to fetch movie details. To use this feature:

1. Obtain an API key from [OMDb API](https://www.omdbapi.com/apikey.aspx)
2. Set the API key in your `.env` file or pass it as a command-line argument

## Website Generation

The application can generate a website to showcase your movie collection:

1. Select option 9 from the menu
2. The application will generate an `index.html` file with all your movies
3. Open the HTML file in any web browser to view your collection

## Requirements

- Python 3.6 or higher
- Requests library (for API integration)

## Application Structure

The application follows an object-oriented design:

1. `IStorage` interface defines the contract for storage backends
2. `StorageCSV` and `StorageJSON` implement the storage interface
3. `MovieApp` handles the business logic and user interaction
4. `OMDbService` handles communication with the OMDb API
