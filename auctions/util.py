import requests


def is_valid_image(image_url):
    image_formats = ("image/png", "image/jpeg", "image/jpg")
    try:
        r = requests.head(image_url)
    except SSLError:
        return False
    if r.headers["content-type"] in image_formats:
        return True
    return False