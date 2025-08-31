# Azure Video Indexer Python Project

## Overview
This project demonstrates how to interact with Azure Video Indexer using Python. It includes example scripts and test files for uploading and processing video files, as well as automating deployment and resource management using Azure CLI.

## Main Azure CLI Commands Used

| Command | Description |
| ------- | ----------- |
| `az login` | Sign in to Azure account. |
| `az group create --name <group> --location <location>` | Create a new resource group in Azure. |
| `az storage account create --name <name> --resource-group <group> --location <location> --sku Standard_LRS` | Create a storage account for storing video files. |
| `az video indexer account create --name <name> --resource-group <group> --location <location>` | Create a Video Indexer account. |
| `az video indexer video upload --account-name <name> --video <file>` | Upload a video to Video Indexer. |
| `az video indexer video get-index --account-name <name> --video-id <id>` | Retrieve the video index and insights. |
| `az group delete --name <group>` | Delete the resource group and all associated resources. |

## Custom Instructions
- Replace placeholders (e.g., `<name>`, `<group>`, `<location>`, `<file>`, `<id>`) with your actual values.
- Ensure you have the necessary permissions and the Azure CLI installed.
- For more details, refer to the official Azure CLI documentation.
