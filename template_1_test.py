

import requests
import json
import os
from dotenv import load_dotenv



# https://github.com/Azure-Samples/azure-video-indexer-samples
# - NO PYTHON EXAMPLE PROVIDED

### Time and Space Complexity Analysis:

# 1. **get_access_token()**:
#    - **Time Complexity**: O(1), as it makes a single HTTP GET request, which is a constant-time operation.
#    - **Space Complexity**: O(1), as it uses a fixed amount of memory for the request and response handling.

# 2. **upload_video()**:
#    - **Time Complexity**: O(n), where n is the size of the video file being uploaded.
#    - **Space Complexity**: O(n), as the video file is loaded into memory for the upload process.

# 3. **get_video_insights()**:
#    - **Time Complexity**: O(1), as it makes a single HTTP GET request, which is a constant-time operation.
#    - **Space Complexity**: O(1), as it uses a fixed amount of memory for the request and response handling.

# 4. **Overall Complexity**:
#    - **Time Complexity**: O(n), dominated by the video upload operation.
#    - **Space Complexity**: O(n), due to the memory required for the video file during upload.



# Mock Data for Testing
# Replace these placeholders with your actual Azure Video Indexer credentials and video file path.
# MOCK_SUBSCRIPTION_KEY = "mock_subscription_key"
# MOCK_LOCATION = "trial"
# MOCK_ACCOUNT_ID = "mock_account_id"
# MOCK_VIDEO_FILE_PATH = "mock_video.mp4"

MOCK_SUBSCRIPTION_KEY = "mock_subscription_key"
MOCK_LOCATION = "trial"
MOCK_ACCOUNT_ID = "1c44359e-c911-48fb-83c5-8546f1cbf577"
MOCK_VIDEO_FILE_PATH = "mock_video.mp4"

# Mock video file creation for testing
with open(MOCK_VIDEO_FILE_PATH, "wb") as mock_video:
    mock_video.write(b"Mock video content for testing purposes.")


# Code Explanation:
# This Python script interacts with the Azure Video Indexer REST API to perform three main tasks:
# 1. Fetch an access token for authentication.
# 2. Upload a video file to the Azure Video Indexer.
# 3. Retrieve insights for the uploaded video.
# The script includes error handling, test cases, and mock data for testing purposes.

# Load environment variables from .env file
load_dotenv()

# Constants
SUBSCRIPTION_KEY = os.getenv("AZURE_VIDEO_INDEXER_SUBSCRIPTION_KEY")
LOCATION = os.getenv("AZURE_VIDEO_INDEXER_LOCATION")
ACCOUNT_ID = os.getenv("AZURE_VIDEO_INDEXER_ACCOUNT_ID")
VIDEO_FILE_PATH = os.getenv("AZURE_VIDEO_INDEXER_VIDEO_FILE_PATH")

# Step 1: Get Access Token
def get_access_token():
    """
    Fetches the access token required for authenticating API requests.
    """
    try:
        url = f"https://api.videoindexer.ai/Auth/{LOCATION}/Accounts/{ACCOUNT_ID}/AccessToken?allowEdit=true"
        headers = {"Ocp-Apim-Subscription-Key": SUBSCRIPTION_KEY}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.text.strip('"')  # Remove quotes from the token
    except requests.RequestException as e:
        print(f"Error fetching access token: {e}")
        return None

# Step 2: Upload Video
def upload_video(access_token):
    """
    Uploads a video file to the Azure Video Indexer.
    """
    try:
        url = f"https://api.videoindexer.ai/{LOCATION}/Accounts/{ACCOUNT_ID}/Videos"
        params = {
            "accessToken": access_token,
            "name": "Sample Video",
            "description": "A sample video for indexing",
            "privacy": "Private"
        }
        with open(VIDEO_FILE_PATH, "rb") as video_file:
            files = {"file": video_file}
            response = requests.post(url, params=params, files=files)
            response.raise_for_status()
            return response.json()  # Return JSON response for further processing
    except requests.RequestException as e:
        print(f"Error uploading video: {e}")
        return None

# Step 3: Get Video Insights
def get_video_insights(access_token, video_id):
    """
    Fetches insights for a specific video.
    """
    try:
        url = f"https://api.videoindexer.ai/{LOCATION}/Accounts/{ACCOUNT_ID}/Videos/{video_id}/Index"
        params = {"accessToken": access_token}
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()  # Return JSON response for insights
    except requests.RequestException as e:
        print(f"Error fetching video insights: {e}")
        return None


# Main Execution with Test Cases
if __name__ == "__main__":
    # Fetch access token
    token = get_access_token()
    if token:
        print("Access Token fetched successfully.")

        # Upload video
        upload_response = upload_video(token)
        if upload_response:
            print("Video uploaded successfully.")
            video_id = upload_response.get("id")  # Extract video ID from response

            # Fetch video insights
            if video_id:
                print("Fetching video insights...")
                insights = get_video_insights(token, video_id)  # Fixed line
                
                if insights:
                    print("Video insights retrieved successfully.")
                    print(json.dumps(insights, indent=2))  # Pretty print insights
                else:
                    print("Failed to retrieve video insights.")
            else:
                print("No video ID found in upload response.")
        else:
            print("Video upload failed.")
    else:
        print("Failed to fetch access token.")

        
# # Main Execution with Test Cases
# if __name__ == "__main__":
#     # Fetch access token
#     token = get_access_token()
#     if token:
#         print("Access Token fetched successfully.")

#         # Upload video
#         upload_response = upload_video(token)
#         if upload_response:
#             print("Video uploaded successfully.")
#             video_id = upload_response.get("id")  # Extract video ID from response

#             # Fetch video insights
#             if video_id:
#                 print("Fetching video insights...")
#                 insights = get_video



