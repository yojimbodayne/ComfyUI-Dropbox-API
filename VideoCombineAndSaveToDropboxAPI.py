import os
import subprocess
import requests
import json
import numpy as np
from tempfile import NamedTemporaryFile

class VideoCombineAndSaveToDropboxAPI:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "frame_rate": ("FLOAT", {"default": 30, "min": 1, "step": 1}),
                "width": ("INT", {"default": 896, "min": 1, "step": 1}),
                "height": ("INT", {"default": 992, "min": 1, "step": 1}),
                "filename_prefix": ("STRING", {"default": "GeneratedVideo"}),
                "format": (["mp4", "webm"],),
                "api_url": ("STRING", {"default": "https://content.dropboxapi.com/2/files/upload"}),
                "access_token": ("STRING", {"forceInput": True}),
                "dropbox_folder_path": ("STRING", {"default": ""}),
            },
            "optional": {
                "images": ("IMAGE",),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("Dropbox File Path",)
    OUTPUT_NODE = True
    CATEGORY = "Dropbox API Manager"  # Updated category
    FUNCTION = "combine_and_upload"

    def combine_and_upload(
        self,
        frame_rate: int,
        width: int,
        height: int,
        filename_prefix: str,
        format: str,
        api_url: str,
        access_token: str,
        dropbox_folder_path: str,
        images=None
    ):
        if images is None or len(images) == 0:
            print("No images provided.")
            return ("",)

        # Ensure the width and height are divisible by 2
        if width % 2 != 0:
            width += 1
        if height % 2 != 0:
            height += 1

        print(f"Processing video with dimensions {width}x{height}")

        # Create a temporary file to save the video
        with NamedTemporaryFile(suffix=f".{format}", delete=False) as temp_video_file:
            temp_video_file_name = temp_video_file.name

        print(f"Temporary video file created at {temp_video_file_name}")

        # Create a pipe to pass frames directly to ffmpeg
        ffmpeg_command = [
            "ffmpeg",
            "-y",  # overwrite output file if exists
            "-f", "rawvideo",
            "-vcodec", "rawvideo",
            "-pix_fmt", "rgb24",
            "-s", f"{width}x{height}",  # size of one frame
            "-r", str(frame_rate),  # frames per second
            "-i", "-",  # input comes from a pipe
            "-an",  # no audio
            "-c:v", "libx264",  # codec to use
            "-pix_fmt", "yuv420p",
            temp_video_file_name  # output to file
        ]

        try:
            print(f"Running ffmpeg with command: {' '.join(ffmpeg_command)}")
            process = subprocess.Popen(ffmpeg_command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            # Convert images to raw bytes and feed to ffmpeg
            for idx, img_tensor in enumerate(images):
                img_np = (img_tensor.cpu().numpy() * 255).astype(np.uint8)
                img_np = np.clip(img_np, 0, 255)
                print(f"Writing frame {idx + 1}/{len(images)} to ffmpeg")
                process.stdin.write(img_np.tobytes())

            # Close stdin after feeding all images
            process.stdin.close()

            # Wait for ffmpeg to finish processing
            stdout, stderr = process.communicate()
            if process.returncode != 0:
                print(f"FFmpeg stdout: {stdout.decode('utf-8')}")
                print(f"FFmpeg stderr: {stderr.decode('utf-8')}")
                os.remove(temp_video_file_name)
                return ("",)

            print(f"Video saved to {temp_video_file_name}")

            # Construct the Dropbox file path
            dropbox_file_path = f"/{dropbox_folder_path.strip('/')}/{filename_prefix}.{format}"

            # Upload the video file to Dropbox
            self.upload_video_to_dropbox(temp_video_file_name, dropbox_file_path, api_url, access_token)

            # Clean up the temporary video file
            os.remove(temp_video_file_name)

            return (dropbox_file_path,)
        except Exception as e:
            print(f"An error occurred: {e}")
            if os.path.exists(temp_video_file_name):
                os.remove(temp_video_file_name)
            return ("",)

    def upload_video_to_dropbox(self, local_file_path, dropbox_file_path, api_url, access_token):
        access_token = access_token.replace("Bearer", "").strip()
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Dropbox-API-Arg': json.dumps({
                "path": dropbox_file_path,
                "mode": "add",
                "autorename": True,
                "mute": False
            }),
            'Content-Type': 'application/octet-stream'
        }

        with open(local_file_path, 'rb') as f:
            video_data = f.read()

        response = requests.post(api_url, headers=headers, data=video_data)
        if response.status_code == 200:
            print(f"Successfully uploaded to Dropbox: {dropbox_file_path}")
        else:
            print(f"Failed to upload to Dropbox. Response: {response.status_code} {response.text}")

