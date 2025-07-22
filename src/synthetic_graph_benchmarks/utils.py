import os
import requests

def download_file(url: str, folder: str) -> str:
    """
    Download a file from the given URL and save it to the specified folder.
    
    Args:
        url (str): The URL of the file to download.
        folder (str): The folder where the file will be saved.
    
    Returns:
        str: The path to the downloaded file.
    """
    os.makedirs(folder, exist_ok=True)
    response = requests.get(url)
    response.raise_for_status()  # Raise an error for bad responses
    filename = url.split("/")[-1]
    filepath = f"{folder}/{filename}"
    
    with open(filepath, "wb") as file:
        file.write(response.content)
    
    return filepath