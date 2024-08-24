from .PostImagesToDropboxAPI import PostImagesToDropboxAPI
from .FetchTokenFromDropbox import FetchTokenFromDropbox
from .PullImagesFromDropboxAPI import PullImagesFromDropboxAPI
from .PostPromptsToDropboxAPI import PostPromptsToDropboxAPI
from .PostVideosToDropboxAPI import PostVideosToDropboxAPI
from .PullVideosFromDropboxAPI import PullVideosFromDropboxAPI
from .VideoCombineAndSaveToDropboxAPI import VideoCombineAndSaveToDropboxAPI

# Register the nodes
NODE_CLASS_MAPPINGS = {
    "PostImagesToDropboxAPI": PostImagesToDropboxAPI,
    "FetchTokenFromDropbox": FetchTokenFromDropbox,
    "PullImagesFromDropboxAPI": PullImagesFromDropboxAPI,
    "PostPromptsToDropboxAPI": PostPromptsToDropboxAPI,
    "PostVideosToDropboxAPI": PostVideosToDropboxAPI,
    "PullVideosFromDropboxAPI": PullVideosFromDropboxAPI,
    "VideoCombineAndSaveToDropboxAPI": VideoCombineAndSaveToDropboxAPI
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "PostImagesToDropboxAPI": "Post Images To Dropbox API",
    "FetchTokenFromDropbox": "Fetch Token From Dropbox",
    "PullImagesFromDropboxAPI": "Pull Images From Dropbox API",
    "PostPromptsToDropboxAPI": "Post Prompts To Dropbox API",
    "PostVideosToDropboxAPI": "Post Videos To Dropbox API",
    "PullVideosFromDropboxAPI": "Pull Videos From Dropbox API",
    "VideoCombineAndSaveToDropboxAPI": "Video Combine And Save To Dropbox API"
}
