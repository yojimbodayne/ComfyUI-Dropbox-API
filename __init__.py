from .PostImagesToDropboxAPI import PostImagesToDropboxAPI
from .FetchTokenFromDropbox import FetchTokenFromDropbox
from .PullImagesFromDropboxAPI import PullImagesFromDropboxAPI
from .PostPromptsToDropboxAPI import PostPromptsToDropboxAPI
from .PullVideosFromDropboxAPI import PullVideosFromDropboxAPI
from .VideoCombineAndExportToDropboxAPI import VideoCombineAndExportToDropboxAPI
from .PullTextFromDropboxAPI import PullTextFromDropboxAPI

# Register the nodes
NODE_CLASS_MAPPINGS = {
    "PostImagesToDropboxAPI": PostImagesToDropboxAPI,
    "FetchTokenFromDropbox": FetchTokenFromDropbox,
    "PullImagesFromDropboxAPI": PullImagesFromDropboxAPI,
    "PostPromptsToDropboxAPI": PostPromptsToDropboxAPI,
    "PullVideosFromDropboxAPI": PullVideosFromDropboxAPI,
    "VideoCombineAndExportToDropboxAPI": VideoCombineAndExportToDropboxAPI,  # Add comma here
    "PullTextFromDropboxAPI": PullTextFromDropboxAPI
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "PostImagesToDropboxAPI": "Post Images To Dropbox API",
    "FetchTokenFromDropbox": "Fetch Token From Dropbox",
    "PullImagesFromDropboxAPI": "Pull Images From Dropbox API",
    "PostPromptsToDropboxAPI": "Post Prompts To Dropbox API",
    "PullVideosFromDropboxAPI": "Pull Videos From Dropbox API",
    "VideoCombineAndExportToDropboxAPI": "Video Combine And Export To Dropbox API",  # Add comma here
    "PullTextFromDropboxAPI": "Pull Text From DropboxAPI"
}