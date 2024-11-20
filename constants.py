import configparser
import os

# Create the parser
parser = configparser.ConfigParser()

# State the path to `config.local`
config_file_path = os.path.join(os.path.dirname(__file__), "config/config.local")

# Read the file
parser.read(config_file_path)

# Access the API key
YOUTUBE_API_KEY = parser.get("Youtube", "API_KEY")
PLAYLIST_ID = parser.get("Youtube", "PLAYLIST_ID")
