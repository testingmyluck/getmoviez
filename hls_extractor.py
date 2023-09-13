import requests
from bs4 import BeautifulSoup
import re
import json # Add the 're' module for regular expressions

# Input your video URL
video_url = ''  # Replace with your video URL

# Make a request to the video URL
response = requests.get(video_url)

if response.status_code == 200:
    video_page = BeautifulSoup(response.text, 'html.parser')



    # Find all <script> tags in the page
    script_tags = video_page.find_all('script')

    # Search for the script tag containing 'html5player.setVideoHLS'
    for script_tag in script_tags:
        script_text = script_tag.get_text()
        if 'html5player.setVideoHLS' in script_text:
            # Use regular expressions to extract the argument inside the function call
            match = re.search(r"html5player\.setVideoHLS\('([^']+)'\)", script_text)
            if match:
                hls_url = match.group(1)

            # Create a dictionary with the extracted information
            video_info = {
                "hls_url": hls_url,
            }

            # Print the extracted information as JSON
            print(json.dumps(video_info, indent=4))
            break  # Exit the loop after finding the desired script

    else:
        print("No 'html5player.setVideoHLS' script found on the page.")

else:
    print("Failed to retrieve the video page.")