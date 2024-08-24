import requests
from .DropboxTokenURL import DROPBOX_URL  # Corrected import

class FetchTokenFromDropbox:
    @staticmethod
    def INPUT_TYPES():
        return {
            "required": {}
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "fetch_token"
    CATEGORY = "Dropbox API Manager"  # Updated category

    def fetch_token(self):
        try:
            # Download the file content directly using the imported URL
            response = requests.get(DROPBOX_URL)
            response.raise_for_status()

            # Read the content of the file directly from the response
            token_content = response.text.strip()

        except requests.RequestException as e:
            raise ValueError(f"Failed to download the file from Dropbox: {e}")

        return (token_content,)

