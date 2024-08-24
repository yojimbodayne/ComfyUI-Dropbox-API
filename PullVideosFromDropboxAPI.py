import json
import requests
import os

class PullVideosFromDropboxAPI:
    def __init__(self):
        self.api_url = "https://api.dropboxapi.com/2/files/list_folder"
        self.content_url = "https://content.dropboxapi.com/2/files/download"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "access_token": ("STRING", {"forceInput": True}),
                "folder_path": ("STRING", {"default": ""}),
                "iteration_index": ("INT", {"default": 0, "min": 0})
            }
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "pull_videos"
    CATEGORY = "Dropbox API Manager"
    OUTPUT_NODE = True

    def pull_videos(self, access_token, folder_path, iteration_index):
        print(f"Starting pull_videos with folder_path: {folder_path}, iteration_index: {iteration_index}")
        
        # Remove 'Bearer' if it's included in the access_token
        access_token = access_token.replace("Bearer", "").strip()
        
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
        
        # List files in the specified folder
        list_files_payload = json.dumps({"path": folder_path})
        try:
            print(f"Sending request to list files at: {self.api_url}")
            list_files_response = requests.post(self.api_url, headers=headers, data=list_files_payload)
            list_files_response.raise_for_status()
            print(f"List files response status: {list_files_response.status_code}")
            response_json = list_files_response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error listing files: {str(e)}")
            return (None,)
        
        files = response_json.get("entries", [])
        
        if not files:
            print("No files found in the specified folder.")
            return (None,)
        
        print(f"Number of files found: {len(files)}")
        
        # Ensure the iteration index is within bounds
        if iteration_index >= len(files):
            print(f"Iteration index {iteration_index} out of bounds. Max index: {len(files) - 1}")
            return (None,)
        
        # Get the file path of the specified video
        file_path = files[iteration_index].get("path_lower")
        print(f"Selected file path: {file_path}")
        
        # Download the video
        download_headers = {
            'Authorization': f'Bearer {access_token}',
            'Dropbox-API-Arg': json.dumps({"path": file_path})
        }
        try:
            print(f"Sending request to download file from: {self.content_url}")
            download_response = requests.post(self.content_url, headers=download_headers)
            download_response.raise_for_status()
            print(f"Download response status: {download_response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Error downloading video: {str(e)}")
            return (None,)
        
        # Save the video to a temporary location
        local_path = os.path.join("/tmp", os.path.basename(file_path))
        with open(local_path, 'wb') as f:
            f.write(download_response.content)
        
        print(f"Video saved to: {local_path}")
        return (local_path,)