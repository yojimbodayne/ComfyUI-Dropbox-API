import requests
import json

class PostPromptsToDropboxAPI:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text_content": ("STRING", {"multiline": True}),
                "api_url": ("STRING", {"default": "https://content.dropboxapi.com/2/files/upload"}),
                "access_token": ("STRING", {"forceInput": True}),
                "file_path": ("STRING", {"default": "/example.txt"}),
                "overwrite": ("BOOLEAN", {"default": False}),
            }
        }

    RETURN_TYPES = ()
    FUNCTION = "post_text"
    CATEGORY = "Dropbox API Manager"  # Updated category
    OUTPUT_NODE = True

    def post_text(self, text_content, api_url, access_token, file_path, overwrite):
        mode = "overwrite" if overwrite else "add"
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/octet-stream',
            'Dropbox-API-Arg': json.dumps({
                "path": file_path,
                "mode": mode,
                "autorename": True,
                "mute": False
            }),
        }

        try:
            print(f"Uploading text to Dropbox at {file_path}")
            response = requests.post(api_url, headers=headers, data=text_content.encode('utf-8'))
            response.raise_for_status()
            print(f"Upload successful: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Error uploading text: {str(e)}")
            return {"result": f"Error: {str(e)}"}

        return {"result": "Upload successful"}
