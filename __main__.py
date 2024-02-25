from ipytv import playlist as tv_playlist
from argparse import ArgumentParser
from pathlib import Path
import re

def parse_arguments():
    parser = ArgumentParser()
    parser.add_argument("-r", "--regex", dest="regex", help="Regex to match the categories", required=True)
    parser.add_argument("-i", "--input", dest="input", help="Path to m3u+ file", required=True, type=Path)
    parser.add_argument("-v", "--verbose", dest="verbose", help="Enable verbose mode", action="store_true")

    return parser.parse_args()

def debug(message: str):
    global verbose
    
    if verbose:
        print("[M3U-CATEGORY-MATCHER:DEBUG] " + message)

def process(arguments):
    debug("Processing...")
    
    try:
        playlist = tv_playlist.loadf(str(arguments.input))
    except UnicodeDecodeError:
        print("Your playlist is not UTF-8 encoded, or has invalid characters. Please convert it to UTF-8.")
        exit(1)
    except Exception as e:
        print("Something went wrong while loading playlist.")
        print(e)
        exit(1)
        
    debug("Playlist loaded.")
    debug("Matching categories...")
    
    try:
        regex = re.compile(arguments.regex)
    except re.error:
        print("Invalid regex provided.")
        exit(1)
    
    if regex.groups != 1:
        print("Regex must have exactly one group to match.")
        exit(1)
        
    # Example:
    # Regex: ### ([a-zA-Z0-9]+) ###
    # Channel 1 name: "### Movies ###"
    # Channel 2 name: "1 HD"
    # Channel 3 name: "2 HD"
    # Channel 4 name: "### News ###"
    # Channel 5 name: "3 HD"
    # Add category "Movies" to channels: 2., 3.
    # Add category "News" to channel 5.
    
    current_category = None
    for index, channel in enumerate(playlist):
        match = regex.match(channel.name)
        if match:
            playlist.remove_channel(index)
            current_category = channel.name
            
            debug(f"Category matched: {current_category}")
        elif current_category:
            debug(f"Adding category {current_category} to channel {channel.name}")
            channel.attributes["group-title"] = current_category
    
    # save playlist
    debug("Saving playlist...")
    with open(arguments.input, "w+", encoding="utf-8") as f:
        f.write(playlist.to_m3u_plus_playlist())
        
    print("All done!")
    print("Thanks for using this script!")

if __name__ == "__main__":
    arguments = parse_arguments()
    verbose = arguments.verbose
    
    process(arguments)