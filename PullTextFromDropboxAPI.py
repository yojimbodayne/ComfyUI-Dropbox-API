import json
import requests

class PullTextFromDropboxAPI:
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

    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("text_content", "error_message")
    FUNCTION = "pull_text"
    CATEGORY = "Dropbox API Manager"
    OUTPUT_NODE = True

    def pull_text(self, access_token, folder_path, iteration_index):
        print(f"Starting pull_text with folder_path: {folder_path}, iteration_index: {iteration_index}")
        
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
            response_json = list_files_response.json()
        except requests.exceptions.RequestException as e:
            return ("", f"Error listing files: {str(e)}")
        
        files = response_json.get("entries", [])
        
        if not files:
            return ("", "No files found in the specified folder.")
        
        # Filter for .txt files
        txt_files = [file for file in files if file['name'].lower().endswith('.txt')]
        
        if not txt_files:
            return ("", "No .txt files found in the specified folder.")
        
        # Ensure the iteration index is within bounds
        if iteration_index >= len(txt_files):
            return ("", f"Iteration index {iteration_index} out of bounds. Max index: {len(txt_files) - 1}")
        
        # Get the file path of the specified text file
        file_path = txt_files[iteration_index].get("path_lower")
        file_name = txt_files[iteration_index].get("name")
        print(f"Selected file path: {file_path}")
        
        # Download the text file
        download_headers = {
            'Authorization': f'Bearer {access_token}',
            'Dropbox-API-Arg': json.dumps({"path": file_path})
        }
        try:
            print(f"Sending request to download file from: {self.content_url}")
            download_response = requests.post(self.content_url, headers=download_headers)
            download_response.raise_for_status()
        except requests.exceptions.RequestException as e:
            return ("", f"Error downloading text file: {str(e)}")
        
        # Process the text file
        try:
            text_content = download_response.text
            print(f"Text file processed. Length: {len(text_content)} characters")
            
            return (text_content, f"Successfully processed text file: {file_name}")
        except Exception as e:
            return ("", f"Error processing text file {file_name}: {str(e)}")