from io import BytesIO, StringIO

import markdown
import requests
from PIL import Image
from requests.exceptions import Timeout

DEFAULT_REQUEST_TIMEOUT = 30


def markdown_to_html_string(markdown_file_location):
    """
    Read the markdown file, converts it into html string and return it
    """
    try:
        with open(markdown_file_location, "r") as f:
            markdown_string = f.read()
        html_string = markdown.markdown(markdown_string)
        return html_string
    except FileNotFoundError:
        raise FileNotFoundError(f"File {markdown_file_location} doesn't exists.")


def is_valid_url(url: str) -> bool:
    if url.startswith("http://") or url.startswith("https://"):
        return True
    return False


def get_image_from_url(url: str):
    try:
        req = requests.get(url=url, timeout=DEFAULT_REQUEST_TIMEOUT)
        image_data = req.content

        if isinstance(image_data, bytes):
            image_data = BytesIO(image_data)
        else:
            image_data = StringIO(image_data)
        img = Image.open(image_data)
        return img
    except Timeout as e:
        raise e
    except Exception as e:
        raise e
