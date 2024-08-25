import os
import json
import subprocess
import numpy as np
import datetime
import torch
from PIL import Image
import requests
import folder_paths
from comfy.utils import ProgressBar

class VideoCombineAndExportToDropboxAPI:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "frame_rate": ("FLOAT", {"default": 30, "min": 1, "step": 1}),
                "format": (["video/mp4", "video/webm"],),
                "filename_prefix": ("STRING", {"default": "output"}),
                "save_output": ("BOOLEAN", {"default": True}),
                "api_key": ("STRING", {"default": "", "multiline": False}),
                "dropbox_folder_path": ("STRING", {"default": "/", "multiline": False}),
            },
            "optional": {
                "images": ("IMAGE",),
                "audio": ("VHS_AUDIO",),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("Dropbox File URL",)
    FUNCTION = "export_video_to_dropbox"
    CATEGORY = "Dropbox API Manager"

    def export_video_to_dropbox(self, frame_rate, format, filename_prefix, save_output, api_key, dropbox_folder_path, images=None, audio=None):
        if images is None:
            raise ValueError("No images provided for video creation.")

        output_path = self.combine_video(images, frame_rate, format, filename_prefix, save_output, audio)
        
        if save_output:
            dropbox_url = self.upload_to_dropbox(output_path, dropbox_folder_path, api_key)
            return (dropbox_url,)
        else:
            return ("Video not saved, no Dropbox upload performed.",)

    def combine_video(self, images, frame_rate, format, filename_prefix, save_output, audio=None):
        output_dir = folder_paths.get_output_directory() if save_output else folder_paths.get_temp_directory()
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{filename_prefix}_{timestamp}.{format.split('/')[-1]}"
        output_path = os.path.join(output_dir, filename)

        ffmpeg_path = "ffmpeg"  # Ensure ffmpeg is in your system PATH
        args = [
            ffmpeg_path, "-y",
            "-f", "rawvideo",
            "-vcodec", "rawvideo",
            "-s", f"{images[0].shape[1]}x{images[0].shape[0]}",
            "-pix_fmt", "rgb24",
            "-r", str(frame_rate),
            "-i", "-",
            "-c:v", "libx264" if format == "video/mp4" else "libvpx-vp9",
            "-pix_fmt", "yuv420p",
            output_path
        ]

        if audio:
            args.extend(["-i", audio, "-c:a", "aac" if format == "video/mp4" else "libopus"])

        process = subprocess.Popen(args, stdin=subprocess.PIPE)

        for img in images:
            process.stdin.write(self.tensor_to_bytes(img).tobytes())

        process.stdin.close()
        process.wait()

        if process.returncode != 0:
            raise RuntimeError(f"FFmpeg failed with error code {process.returncode}")

        return output_path

    def upload_to_dropbox(self, local_file_path, dropbox_folder_path, api_key):
        dropbox_path = f"{dropbox_folder_path.rstrip('/')}/{os.path.basename(local_file_path)}"
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Dropbox-API-Arg": json.dumps({
                "path": dropbox_path,
                "mode": "add",
                "autorename": True,
                "mute": False
            }),
            "Content-Type": "application/octet-stream"
        }

        with open(local_file_path, "rb") as file:
            response = requests.post(
                "https://content.dropboxapi.com/2/files/upload",
                headers=headers,
                data=file
            )

        if response.status_code != 200:
            raise Exception(f"Failed to upload to Dropbox. Status code: {response.status_code}, Response: {response.text}")

        return self.create_shared_link(dropbox_path, api_key)

    def create_shared_link(self, file_path, api_key):
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "path": file_path,
            "settings": {"requested_visibility": "public"}
        }

        response = requests.post(
            "https://api.dropboxapi.com/2/sharing/create_shared_link_with_settings",
            headers=headers,
            json=data
        )

        if response.status_code != 200:
            raise Exception(f"Failed to create shared link. Status code: {response.status_code}, Response: {response.text}")

        return response.json()['url']

    @staticmethod
    def tensor_to_bytes(tensor):
        return (tensor.cpu().numpy() * 255).astype(np.uint8)