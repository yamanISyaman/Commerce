import requests
from .models import User, Auction, Bid, Comment, WatchList
from .forms import CreateForm, BidForm, CommentForm


def is_valid_image(image_url):
    image_formats = ("image/png", "image/jpeg", "image/jpg", "image/svg")
    try:
        r = requests.head(image_url)
    except SSLError:
        return False
    if r.headers["content-type"] in image_formats:
        return True
    return False


def listing_attrs(auction, username, bm=None, cm=None):
    attrs = {
        "auction": auction,
        "close_input": False,
        "bidform": BidForm(),
        "commentform": CommentForm(),
        "comments": Comment.objects.filter(auction =auction),
        "show_winner": False,
        "signed": True

    }
    if not username.is_authenticated:
        attrs["signed"] = False
        return attrs
    owner = auction.user
    user = User.objects.get(username=username)
    wl = WatchList.objects.filter(user=user, auction=auction)
    if cm:
        attrs["commentmessage"] = cm
    if bm:
        attrs["message"] = bm
    attrs["in_wl"] = True if wl else False
    if user == owner:
        attrs["close_input"] = True
    if user == auction.winner:
        attrs["show_winner"] = True

    return attrs






