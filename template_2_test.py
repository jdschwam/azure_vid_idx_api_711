
# Here’s an example of how to use the Azure Cognitive Search REST API to create an image 
# index. This involves creating a data source, an index, an indexer, and optionally a 
# skillset for image processing. Below is a concise example in Python using the requests 
# library:


# ######################################################################
#! Example 1: Create an Index for Images
# ######################################################################

import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Azure Search service details
service_name = os.getenv("AZURE_SEARCH_SERVICE_NAME")
api_version = "2021-04-30-Preview"
api_key = os.getenv("AZURE_SEARCH_API_KEY")

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


# ######################################################################
#! Example 2: Create a Data Source for Blob Storage
# ######################################################################

data_source_endpoint = f"https://{service_name}.search.windows.net/datasources?api-version={api_version}"

data_source = {
    "name": "image-blob-datasource",
    "type": "azureblob",
    "credentials": {"connectionString": "your-blob-storage-connection-string"},
    "container": {"name": "your-container-name"}
}

response = requests.put(data_source_endpoint, headers=headers, data=json.dumps(data_source))
print(response.status_code, response.json())


# ######################################################################
#! Example 3: Create an Indexer to Populate the Index
# ######################################################################

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

# Notes:
# Replace placeholders like your-search-service-name, your-api-key, and your-blob-storage-connection-string with your actual Azure service details.
# You can enhance this by adding a skillset for image analysis (e.g., extracting tags or descriptions using Azure Cognitive Services).

# Let me know if you'd like further clarification or additional examples!