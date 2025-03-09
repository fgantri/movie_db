import os
import sys

from movie_app import MovieApp
from storage_json import StorageJson
from storage_csv import StorageCsv


def print_usage():
    """Print usage instructions"""
    print("Usage: python main.py [storage_type]")
    print("  storage_type: 'csv' or 'json' (default: csv)")
    print("")
    print("Example: python main.py json")


def main():
    """Entry point for the movie database application"""
    # Parse command line arguments for storage type
    storage_type = "csv"  # Default storage type
    
    if len(sys.argv) > 1:
        arg = sys.argv[1].lower()
        if arg in ["csv", "json"]:
            storage_type = arg
        else:
            print(f"Unknown storage type: {arg}")
            print_usage()
            return
    
    # Initialize the appropriate storage backend
    try:
        if storage_type == "csv":
            file_path = 'movies.csv'
            storage = StorageCsv(file_path, ",")
            print(f"Using CSV storage: {file_path}")
        else:  # json
            file_path = 'movies.json'
            storage = StorageJson(file_path)
            print(f"Using JSON storage: {file_path}")
        
        # Run the application
        movie_app = MovieApp(storage)
        movie_app.run()
    except Exception as e:
        print(f"An error occurred while starting the application: {str(e)}")
        print("Please check if you have proper permissions or if the storage files are not corrupted.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nApplication terminated by user.")
    except Exception as e:
        print(f"\nUnexpected error: {str(e)}")
