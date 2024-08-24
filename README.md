# ComfyUI-Dropbox-API

This custom node package for ComfyUI allows users to interact with Dropbox API, enabling image, text, and video uploads, downloads, and management directly from ComfyUI workflows.

## Setup Instructions

Before using the Dropbox API nodes, you need to set up your Dropbox API token:

1. Obtain a Dropbox API token:
   - Go to the Dropbox App Console in the developer settings.
   - Create a new app or use an existing one.
   - Generate an access token for your app.

2. Create a `token.txt` file:
   - In your Dropbox account, create a new text file named `token.txt`.
   - Paste your Dropbox API token into this file. The file should contain only the token.

3. Configure the DropboxTokenURL:
   - In the `DropboxTokenURL.py` file, locate the variable for the Dropbox token URL.
   - Replace the placeholder URL with the direct link to your `token.txt` file in Dropbox.

## Available Nodes

- Post Images To Dropbox API
- Pull Images From Dropbox API
- Post Videos To Dropbox API (currently not functional)
- Pull Videos From Dropbox API
- Video Combine And Save To Dropbox API (currently not functional)

## Usage Notes

- Ensure that your Dropbox token has the necessary permissions for the operations you want to perform.
- The "Post Videos To Dropbox API" and "Video Combine And Save To Dropbox API" nodes are currently not functioning correctly. We are working on fixing these issues.

## Troubleshooting

If you encounter any issues:
- Verify that your Dropbox API token is correct and has not expired (expires every 4 hours or so).
- Check that the `token.txt` file in your Dropbox contains only the API token.
- Ensure that the URL in `DropboxTokenURL.py` is correct and accessible.

## Support

For support, please open an issue in the GitHub repository or send me a message.

## Contributing

Contributions to improve the nodes or fix current issues are welcome. Please submit a pull request or open an issue to discuss proposed changes.

## License

[2024YojimboDayne_license2Ill]