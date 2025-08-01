

https://github.com/Azure-Samples/azure-video-indexer-samples
- NO PYTHON EXAMPLE PROVIDED





Plaintext
Copy code
### Time and Space Complexity Analysis:

1. **get_access_token()**:
   - **Time Complexity**: O(1), as it makes a single HTTP GET request, which is a constant-time operation.
   - **Space Complexity**: O(1), as it uses a fixed amount of memory for the request and response handling.

2. **upload_video()**:
   - **Time Complexity**: O(n), where n is the size of the video file being uploaded.
   - **Space Complexity**: O(n), as the video file is loaded into memory for the upload process.

3. **get_video_insights()**:
   - **Time Complexity**: O(1), as it makes a single HTTP GET request, which is a constant-time operation.
   - **Space Complexity**: O(1), as it uses a fixed amount of memory for the request and response handling.

4. **Overall Complexity**:
   - **Time Complexity**: O(n), dominated by the video upload operation.
   - **Space Complexity**: O(n), due to the memory required for the video file during upload.

Python
Copy code
# Mock Data for Testing
# Replace these placeholders with your actual Azure Video Indexer credentials and video file path.
MOCK_SUBSCRIPTION_KEY = "mock_subscription_key"
MOCK_LOCATION = "trial"
MOCK_ACCOUNT_ID = "mock_account_id"
MOCK_VIDEO_FILE_PATH = "mock_video.mp4"

# Mock video file creation for testing
with open(MOCK_VIDEO_FILE_PATH, "wb") as mock_video:
    mock_video.write(b"Mock video content for testing purposes.")

Python
Copy code
# Code Explanation:
# This Python script interacts with the Azure Video Indexer REST API to perform three main tasks:
# 1. Fetch an access token for authentication.
# 2. Upload a video file to the Azure Video Indexer.
# 3. Retrieve insights for the uploaded video.
# The script includes error handling, test cases, and mock data for testing purposes.

import requests

# Constants
SUBSCRIPTION_KEY = MOCK_SUBSCRIPTION_KEY
LOCATION = MOCK_LOCATION
ACCOUNT_ID = MOCK_ACCOUNT_ID
VIDEO_FILE_PATH = MOCK_VIDEO_FILE_PATH

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
                insights = get_video







# Here’s an example of how to use the Azure Cognitive Search REST API to create an image index. This involves creating a data source, an index, an indexer, and optionally a skillset for image processing. Below is a concise example in Python using the requests library:

Example 1: Create an Index for Images
Python
Copy code
import requests
import json

# Azure Search service details
service_name = "your-search-service-name"
api_version = "2021-04-30-Preview"
api_key = "your-api-key"

# Endpoint URL
endpoint = f"https://{service_name}.search.windows.net/indexes?api-version={api_version}"

# Define the index schema
index_schema = {
    "name": "image-index",
    "fields": [
        {"name": "id", "type": "Edm.String", "key": True, "filterable": True},
        {"name": "imageUrl", "type": "Edm.String", "searchable": False},
        {"name": "tags", "type": "Collection(Edm.String)", "searchable": True},
        {"name": "description", "type": "Edm.String", "searchable": True}
    ]
}

# Create the index
headers = {
    "Content-Type": "application/json",
    "api-key": api_key
}
response = requests.put(endpoint, headers=headers, data=json.dumps(index_schema))

print(response.status_code, response.json())

Example 2: Create a Data Source for Blob Storage
Python
Copy code
data_source_endpoint = f"https://{service_name}.search.windows.net/datasources?api-version={api_version}"

data_source = {
    "name": "image-blob-datasource",
    "type": "azureblob",
    "credentials": {"connectionString": "your-blob-storage-connection-string"},
    "container": {"name": "your-container-name"}
}

response = requests.put(data_source_endpoint, headers=headers, data=json.dumps(data_source))
print(response.status_code, response.json())

Example 3: Create an Indexer to Populate the Index
Python
Copy code
indexer_endpoint = f"https://{service_name}.search.windows.net/indexers?api-version={api_version}"

indexer = {
    "name": "image-indexer",
    "dataSourceName": "image-blob-datasource",
    "targetIndexName": "image-index",
    "fieldMappings": [
        {"sourceFieldName": "metadata_storage_path", "targetFieldName": "imageUrl"}
    ]
}

response = requests.put(indexer_endpoint, headers=headers, data=json.dumps(indexer))
print(response.status_code, response.json())

Notes:
Replace placeholders like your-search-service-name, your-api-key, and your-blob-storage-connection-string with your actual Azure service details.
You can enhance this by adding a skillset for image analysis (e.g., extracting tags or descriptions using Azure Cognitive Services).

Let me know if you'd like further clarification or additional examples!