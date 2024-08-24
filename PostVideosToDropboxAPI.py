import json
import requests
from io import BytesIO

class PostVideosToDropboxAPI:
    def __init__(self):
        self.api_url = "https://content.dropboxapi.com/2/files/upload"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "video_path": ("STRING", {"forceInput": True}),  # Path to the video file
                "api_object_id": ("STRING", {"forceInput": True}),  # Object ID for API
                "api_key": ("STRING", {"forceInput": True}),  # API Key for authorization
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("status",)
    FUNCTION = "post_video"
    CATEGORY = "Dropbox API Manager"
    OUTPUT_NODE = True

    def post_video(self, video_path, api_object_id, api_key):
        # Remove 'Bearer' if it's included in the api_key
        api_key = api_key.replace("Bearer", "").strip()
        
        # Set up headers for the request
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Dropbox-API-Arg': json.dumps({
                "path": api_object_id,
                "mode": "add",
                "autorename": True,
                "mute": False
            }),
            'Content-Type': 'application/octet-stream'
        }

        # Ensure the file is an MP4 video
        if not video_path.endswith(".mp4"):
            return ("Error: The file must be in .mp4 format.",)

        # Open the video file in binary mode
        try:
            with open(video_path, 'rb') as video_file:
                video_data = video_file.read()

            # Send the POST request with the video
            response = requests.post(self.api_url, headers=headers, data=video_data)
            response.raise_for_status()
            print(f"Video posted successfully to {self.api_url}\nResponse: {response.json()}")
            return ("Video posted successfully",)
        except FileNotFoundError:
            return (f"Error: File not found at {video_path}",)
        except requests.exceptions.RequestException as e:
            print(f"Error posting video: {str(e)}")
            return (f"Error posting video: {str(e)}",)

# Do not include these mappings here if they are in __init__.py
# NODE_CLASS_MAPPINGS = {
#     "PostVideosToDropboxAPI": PostVideosToDropboxAPI
# }
# 
# NODE_DISPLAY_NAME_MAPPINGS = {
#     "PostVideosToDropboxAPI": "Post Videos To Dropbox API"
# }