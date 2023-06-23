import requests
from .models import User, Auction, Bid, Comment
from .forms import CreateForm, BidForm, CommentForm


def is_valid_image(image_url):
    image_formats = ("image/png", "image/jpeg", "image/jpg")
    try:
        r = requests.head(image_url)
    except SSLError:
        return False
    if r.headers["content-type"] in image_formats:
        return True
    return False


def listing_attrs(auction, username, bm=None, cm=None):
    owner = auction.user
    user = User.objects.get(username=username)
    attrs = {
                "auction": auction,
                "close_input": False,
                "bidform": BidForm(),
                "commentform": CommentForm(),
                "comments": Comment.objects.filter(auction =auction)
    }
    if cm:
        attrs["commentmessage"] = cm
    if bm:
        attrs["message"] = bm
    if user == owner:
        attrs["close_input"] = True

    return attrs






