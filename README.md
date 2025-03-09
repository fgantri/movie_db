# Movie Database Application

A simple command-line application for managing a collection of movies, with support for multiple storage backends (CSV and JSON).

## Features

- List all movies in the database
- Add new movies with title, year, rating, and poster URL
- Delete movies by title
- Update movie ratings
- View movie statistics (average rating, median rating, best and worst movies)
- Get random movie recommendations
- Search for movies by title
- Sort movies by rating or year
- Filter movies by rating, start year, and end year

## Usage

```
python main.py [storage_type]
```

Where `storage_type` is optional and can be one of:
- `csv` - Use CSV file storage (default)
- `json` - Use JSON file storage

Example:
```
python main.py json
```

## Data Storage

The application supports two storage backends:

1. **CSV Storage**: Stores data in a comma-separated values file (`movies.csv`)
2. **JSON Storage**: Stores data in a JSON file (`movies.json`)

The storage files are created automatically if they don't exist.

## Files

- `main.py`: Entry point for the application
- `movie_app.py`: The main application logic
- `istorage.py`: Interface definition for storage backends
- `storage_csv.py`: CSV file storage implementation
- `storage_json.py`: JSON file storage implementation
- `input_validator.py`: Utilities for validating user input
- `output_formatter.py`: Utilities for formatting output

## Requirements

- Python 3.6 or higher

## Application Structure

The application follows an object-oriented design:

1. `IStorage` interface defines the contract for storage backends
2. `StorageCSV` and `StorageJSON` implement the storage interface
3. `MovieApp` handles the business logic and user interaction
