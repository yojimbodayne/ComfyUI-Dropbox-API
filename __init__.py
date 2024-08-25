from .PostImagesToDropboxAPI import PostImagesToDropboxAPI
from .FetchTokenFromDropbox import FetchTokenFromDropbox
from .PullImagesFromDropboxAPI import PullImagesFromDropboxAPI
from .PostPromptsToDropboxAPI import PostPromptsToDropboxAPI
from .PullVideosFromDropboxAPI import PullVideosFromDropboxAPI
from .VideoCombineAndExportToDropboxAPI import VideoCombineAndExportToDropboxAPI  # Add this line
from .PullTextFromDropboxAPI import PullTextFromDropboxAPI  # Add this line


# Register the nodes
NODE_CLASS_MAPPINGS = {
    "PostImagesToDropboxAPI": PostImagesToDropboxAPI,
    "FetchTokenFromDropbox": FetchTokenFromDropbox,
    "PullImagesFromDropboxAPI": PullImagesFromDropboxAPI,
    "PostPromptsToDropboxAPI": PostPromptsToDropboxAPI,
    "PullVideosFromDropboxAPI": PullVideosFromDropboxAPI,
    "VideoCombineAndExportToDropboxAPI": VideoCombineAndExportToDropboxAPI  # Add this line
    "PullTextFromDropboxAPI": PullTextFromDropboxAPI
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "PostImagesToDropboxAPI": "Post Images To Dropbox API",
    "FetchTokenFromDropbox": "Fetch Token From Dropbox",
    "PullImagesFromDropboxAPI": "Pull Images From Dropbox API",
    "PostPromptsToDropboxAPI": "Post Prompts To Dropbox API",
    "PullVideosFromDropboxAPI": "Pull Videos From Dropbox API",
    "VideoCombineAndExportToDropboxAPI": "Video Combine And Export To Dropbox API"  # Add this line
    "PullTextFromDropboxAPI": "Pull Text From DropboxAPI"
}