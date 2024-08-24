import requests
from datetime import datetime
import json
from PIL import Image
import numpy as np
import io

class PostImagesToDropboxAPI:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "folder_location": ("STRING", {"default": "/"}),
                "folder_by_date": ("BOOLEAN", {"default": False}),
                "optional_filename_text": ("STRING", {"default": ""}),
                "file_extension": ("STRING", {"default": ".png"}),
                "images": ("IMAGE",),
                "api_key": ("STRING", {"default": ""}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("metadata",)
    FUNCTION = "upload_image_to_dropbox"
    CATEGORY = "Dropbox API Manager"

    def construct_auth_body_text(self, folder_location, folder_by_date, optional_filename_text, file_extension=".png"):
        api_object_id = folder_location.rstrip('/')

        if folder_by_date:
            current_date = datetime.now().strftime("%Y%m%d")
            api_object_id = f"{api_object_id}/{current_date}"

        current_time = datetime.now().strftime("%H%M%S")
        filename = current_time

        if optional_filename_text:
            filename = f"{filename}_{optional_filename_text}"

        api_object_id = f"{api_object_id}/{filename}{file_extension}"

        auth_body_text = {
            "path": api_object_id,
            "mode": "add",
            "autorename": True,
            "mute": False
        }

        return json.dumps(auth_body_text)

    def upload_image_to_dropbox(self, folder_location, folder_by_date, optional_filename_text, file_extension, images, api_key):
        auth_body_text = self.construct_auth_body_text(folder_location, folder_by_date, optional_filename_text, file_extension)

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/octet-stream",
            "Dropbox-API-Arg": auth_body_text
        }

        image_np = (images[0].cpu().numpy() * 255).astype(np.uint8)
        image_pil = Image.fromarray(image_np)
        image_bytes = io.BytesIO()
        image_pil.save(image_bytes, format=file_extension.lstrip(".").upper())
        image_bytes = image_bytes.getvalue()

        try:
            response = requests.post(
                "https://content.dropboxapi.com/2/files/upload",
                headers=headers,
                data=image_bytes
            )
            response.raise_for_status()
            return (response.text,)
        except requests.exceptions.RequestException as e:
            return (f"Error uploading to Dropbox: {str(e)}",)

# Do not include these mappings here if they are in __init__.py
# NODE_CLASS_MAPPINGS = {
#     "PostImagesToDropboxAPI": PostImagesToDropboxAPI
# }
# 
# NODE_DISPLAY_NAME_MAPPINGS = {
#     "PostImagesToDropboxAPI": "Post Images To Dropbox API"
# }