import requests
import os
import time

def scrape_images_from_pages(
    base_url_for_pages,
    parent_page_name_prefix,
    num_parent_pages, # This now represents the *last* page number to process
    start_page_num=1, # New parameter with a default of 1
    image_extension=".jpg",
    max_images_per_page=200, # Safety limit for images per parent page
    output_directory="scraped_pictures_by_page"
):
    """
    Scrapes images from a series of parent pages, where each page contains sequentially named images.
    It assumes images are located in a path relative to the parent page URL, e.g.,
    if parent page is "http://example.com/path/name_1", images are expected at
    "http://example.com/path/name_1/1.jpg", "http://example.com/path/name_1/2.jpg", etc.

    Args:
        base_url_for_pages (str): The base URL part before the parent page name and its number.
                                  Example: "http://example.com/articles"
                                  (Script will form URLs like "http://example.com/articles/name_1")
        parent_page_name_prefix (str): The prefix for parent page names.
                                       Example: "name" (will form "name_1", "name_2")
        num_parent_pages (int): The *last* parent page number to process (e.g., if you want up to page 500, set this to 500).
        start_page_num (int): The parent page number to start scraping from (e.g., 101). Defaults to 1.
        image_extension (str): The file extension for the images (e.g., ".jpg"). Must include the dot.
        max_images_per_page (int): Max number of images to check for per parent page before stopping.
        output_directory (str): Directory to save images, with subdirs for each parent page.
    """

    # Basic input validation
    if not base_url_for_pages.startswith(("http://", "https://")):
        print(f"Error: base_url_for_pages ('{base_url_for_pages}') must be a valid URL starting with http:// or https://.")
        return
    if not image_extension.startswith("."):
        print(f"Error: image_extension ('{image_extension}') must start with a dot (e.g., '.jpg').")
        return
    if not isinstance(max_images_per_page, int) or max_images_per_page <= 0:
        print(f"Error: max_images_per_page ({max_images_per_page}) must be a positive integer.")
        return
    if not isinstance(num_parent_pages, int) or num_parent_pages <= 0:
        print(f"Error: num_parent_pages ({num_parent_pages}) must be a positive integer representing the last page to process.")
        return
    if not isinstance(start_page_num, int) or start_page_num <= 0:
        print(f"Error: start_page_num ({start_page_num}) must be a positive integer.")
        return
    if start_page_num > num_parent_pages:
        print(f"Error: start_page_num ({start_page_num}) cannot be greater than num_parent_pages ({num_parent_pages}). Nothing to scrape.")
        return

    # Create the main output directory if it doesn't exist
    if not os.path.exists(output_directory):
        try:
            os.makedirs(output_directory)
            print(f"Created main directory: {output_directory}")
        except OSError as e:
            print(f"Error creating main directory {output_directory}: {e}")
            return

    print(f"Starting scraping from parent page {start_page_num} up to {num_parent_pages}...")
    print(f"Image URLs will be constructed like: {base_url_for_pages}/{parent_page_name_prefix}_[page_num]/[image_num]{image_extension}")

    for page_num in range(start_page_num, num_parent_pages + 1):
        parent_page_segment = f"{parent_page_name_prefix}_{page_num}"
        current_page_image_base_url = f"{base_url_for_pages.rstrip('/')}/{parent_page_segment}"
        page_specific_output_dir = os.path.join(output_directory, parent_page_segment)

        print(f"\nProcessing parent page: {current_page_image_base_url}/")

        if not os.path.exists(page_specific_output_dir):
            try:
                os.makedirs(page_specific_output_dir)
                print(f"  Created subdirectory: {page_specific_output_dir}")
            except OSError as e:
                print(f"  Error creating subdirectory {page_specific_output_dir}: {e}. Skipping this parent page.")
                continue

        images_downloaded_for_this_page = 0
        for image_idx in range(1, max_images_per_page + 1):
            image_filename = f"{image_idx}{image_extension}"
            full_image_url = f"{current_page_image_base_url}/{image_filename}"
            output_image_path = os.path.join(page_specific_output_dir, image_filename)

            if os.path.exists(output_image_path):
                print(f"  Skipping already downloaded image: {output_image_path}")
                images_downloaded_for_this_page +=1
                continue

            try:
                response = requests.get(full_image_url, stream=True, timeout=10)

                if response.status_code == 200: # OK
                    with open(output_image_path, 'wb') as f:
                        for chunk in response.iter_content(chunk_size=8192):
                            f.write(chunk)
                    print(f"  Successfully downloaded: {full_image_url} -> {output_image_path}")
                    images_downloaded_for_this_page += 1
                elif response.status_code == 404: # Not Found
                    if image_idx == 1:
                        print(f"  No images found for {parent_page_segment} (e.g., {image_filename} returned 404).")
                    else:
                        print(f"  End of images for {parent_page_segment} ({image_filename} returned 404). "
                              f"{images_downloaded_for_this_page} images downloaded for this page.")
                    break
                else:
                    print(f"  HTTP error {response.status_code} for {full_image_url}. Skipping further images for this page.")
                    break

            except requests.exceptions.HTTPError as http_err:
                print(f"  HTTP error occurred for {full_image_url}: {http_err}. Skipping further images for this page.")
                break
            except requests.exceptions.ConnectionError as conn_err:
                print(f"  Connection error for {full_image_url}: {conn_err}. Skipping further images for this page.")
                break
            except requests.exceptions.Timeout as timeout_err:
                print(f"  Timeout occurred for {full_image_url}: {timeout_err}. Skipping further images for this page.")
                break
            except requests.exceptions.RequestException as req_err:
                print(f"  An error occurred while requesting {full_image_url}: {req_err}. Skipping further images for this page.")
                break
            
            # Optional: Add a small delay to be polite to the server
            # time.sleep(0.1) # Sleep for 0.1 seconds

        if images_downloaded_for_this_page == 0 and image_idx > 1 and image_idx < max_images_per_page :
            pass
        elif images_downloaded_for_this_page > 0 and image_idx == max_images_per_page:
             print(f"  Reached max_images_per_page ({max_images_per_page}) for {parent_page_segment}. "
                   f"{images_downloaded_for_this_page} images downloaded for this page.")

    print("\nImage scraping process from parent pages completed.")

if __name__ == "__main__":
    # --- Configuration ---
    # IMPORTANT: You MUST change these values to match your target website.

    # 1. The base URL path BEFORE the "/name_1", "/name_2" part.
    config_base_url = "http://www.example.com/files/documents"  # <<< CHANGE THIS

    # 2. The prefix part of the parent page names (e.g., "name" in "name_1", "name_2").
    config_page_prefix = "name"  # <<< CHANGE THIS

    # 3. The parent page number to START scraping from.
    #    To start from the beginning (e.g., page 1), set this to 1.
    config_start_page = 101  # <<< CHANGE THIS (e.g., to start from page 101)

    # 4. The LAST parent page number to process.
    #    Example: If you want to scrape from page 101 up to page 200, set this to 200.
    #    This value must be >= config_start_page.
    config_last_page = 200   # <<< CHANGE THIS (e.g., to process up to page 200)

    # 5. File extension of the images you want to download (e.g., ".jpg", ".png", ".gif").
    config_image_ext = ".jpg"  # <<< CHANGE THIS

    # 6. Maximum number of images (1.jpg, 2.jpg, ...) to attempt to find on each parent page.
    config_max_img_per_page = 50  # <<< CHANGE THIS

    # 7. Name of the main local directory where subdirectories will be saved.
    config_output_folder = "downloaded_website_images"  # <<< CHANGE THIS if desired
    # --- End Configuration ---

    # Call the main scraping function with the configured parameters
    scrape_images_from_pages(
        base_url_for_pages=config_base_url,
        parent_page_name_prefix=config_page_prefix,
        num_parent_pages=config_last_page,       # This is the LAST page number
        start_page_num=config_start_page,       # This is the STARTING page number
        image_extension=config_image_ext,
        max_images_per_page=config_max_img_per_page,
        output_directory=config_output_folder
    )