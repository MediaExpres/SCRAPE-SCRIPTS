# scrape_nested_images.py

## Overview

`scrape_nested_images.py` is a flexible Python script for bulk-downloading images that are organized in nested directories on a website. It is designed for cases where images are accessible via URLs following a sequential, predictable pattern, such as:

```
http://example.com/gallery/name_1/1.jpg
http://example.com/gallery/name_1/2.jpg
...
http://example.com/gallery/name_2/1.jpg
...
```

The script iterates over a range of "parent pages" (e.g., `name_1`, `name_2`, etc.), and within each, attempts to download images named sequentially (`1.jpg`, `2.jpg`, ...), saving them into organized local folders.  
**You can now specify both the starting and ending parent page numbers.**

## Features

- Downloads images from sequentially named parent pages and nested image sequences.
- **Configurable starting and ending parent page numbers** (e.g., scrape from page 101 to 200).
- Automatic creation of output directories for organized storage.
- Configurable number of parent pages and maximum images per page.
- Handles HTTP errors and skips already-downloaded images.
- Customizable file extensions and output directory.
- Polite to servers (optional delay between downloads).

## Requirements

- Python 3.6+
- [requests](https://pypi.org/project/requests/)

Install dependencies with:

```bash
pip install requests
```

## Usage

1. **Edit Configuration:**

At the bottom of the script (inside the `if __name__ == "__main__":` block), change the following variables to match your target website:

```python
config_base_url = "http://www.example.com/files/documents"  # Base URL before the parent page name
config_page_prefix = "name"  # Prefix for parent pages (e.g., "name_1", "name_2", ...)
config_start_page = 101  # Parent page number to START scraping from (e.g., 1 or 101)
config_last_page = 200   # LAST parent page number to process (must be >= config_start_page)
config_image_ext = ".jpg"  # Image file extension (e.g., ".jpg", ".png")
config_max_img_per_page = 50  # Max images to try per parent page
config_output_folder = "downloaded_website_images"  # Output directory
```

2. **Run the Script:**

```bash
python scrape_nested_images.py
```

3. **Check Output:**

Downloaded images will be saved in the specified output directory, with subdirectories for each parent page.

## Example

Suppose you want to download images from:

- `http://mysite.com/gallery/set_101/1.jpg`
- `http://mysite.com/gallery/set_101/2.jpg`
- ...
- `http://mysite.com/gallery/set_150/1.jpg`

Set these variables:

```python
config_base_url = "http://mysite.com/gallery"
config_page_prefix = "set"
config_start_page = 101
config_last_page = 150
config_image_ext = ".jpg"
config_max_img_per_page = 10
config_output_folder = "mysite_images"
```

## Notes

- **Respect website rules:** Always check the site's robots.txt and terms of use before scraping.
- **Timeouts and Errors:** The script handles HTTP errors gracefully and skips pages/images it cannot download.
- **Performance:** You may uncomment the `time.sleep()` line in the script to introduce a delay between requests if scraping a large number of images.

## Troubleshooting

- **No images downloaded:** Double-check your base URL and parent page prefix.
- **Permission errors:** Ensure you have write access to the output folder.
- **Connection/Timeout errors:** Check your internet connection, or try increasing the timeout in the script.

## License

MIT License. See [LICENSE](LICENSE) for details.

## Author

Maintained by [MediaExpres](https://github.com/MediaExpres).

---

**Happy scraping!**
