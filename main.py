import requests
import json
import os

def download_images_from_safebooru(url, download_path="."):
    """
    Downloads images from a Safebooru JSON API endpoint.

    Args:
        url (str): The URL of the Safebooru JSON API.
        download_path (str, optional): The directory to save the downloaded images. Defaults to the current directory.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes
        data = response.json()

        if not isinstance(data, list):
            print("Error: Expected a list of posts in the JSON response.")
            return

        os.makedirs(download_path, exist_ok=True)
        downloaded_count = 0

        for i, post in enumerate(data):
            if downloaded_count >= 301:
                break

            if 'file_url' in post:
                file_url = post['file_url']
                try:
                    image_response = requests.get(file_url, stream=True)
                    image_response.raise_for_status()

                    file_extension = os.path.splitext(file_url)[1]
                    filename = f"{downloaded_count:03d}{file_extension}"
                    filepath = os.path.join(download_path, filename)

                    with open(filepath, 'wb') as f:
                        for chunk in image_response.iter_content(chunk_size=8192):
                            f.write(chunk)
                    print(f"Downloaded: {filename}")
                    downloaded_count += 1
                except requests.exceptions.RequestException as e:
                    print(f"Error downloading image from {file_url}: {e}")
            else:
                print(f"Warning: 'file_url' not found in post {i}.")

        print(f"\nSuccessfully downloaded {downloaded_count} images to '{download_path}'.")

    except requests.exceptions.RequestException as e:
        print(f"Error fetching JSON from {url}: {e}")
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    json_url = "https://safebooru.org/index.php?page=dapi&s=post&q=index&tags=yuuka_%28blue_archive%29+&limit=300&json=1"
    download_directory = "images"  # You can change this to your desired directory
    download_images_from_safebooru(json_url, download_directory)
