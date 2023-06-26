from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone


from .models import User, Auction, Bid, Comment, WatchList
from .forms import CreateForm, BidForm, CommentForm
from .util import is_valid_image, listing_attrs



def index(request):
    listings = Auction.objects.filter(closed=False)
    return render(request, "auctions/index.html", {"listings": listings})


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


@login_required
def create(request):
    if request.method == "POST":
        form = CreateForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = User.objects.get(username=request.user)
            if is_valid_image(data["image"]):
                new_auction = Auction(
user=user,
title=data["title"], 
price=data["price"], 
description=data["description"], 
image=data["image"],
date=timezone.now(), category=data["category"],
winner=None,
closed=False
                )
                new_auction.save()
                return HttpResponseRedirect(reverse("index"))
            else:
                return render(request, "auctions/create.html", {
                "form": form,
                "message": "Invalid Image URL"
            })
        else:
            return render(request, "auctions/create.html", {
                "form": form,
                "message": "Invalid Data"
            })
        
    else:
        return render(request, "auctions/create.html", {"form": CreateForm()})


def listing_view(request, id=1):
    auction = Auction.objects.get(id=id)
    return render(request, "auctions/listing.html", listing_attrs(auction, request.user))


@login_required
def add_bid(request, id):
    if request.method == "POST":
        auction = Auction.objects.get(id=id)
        user = User.objects.get(username=request.user)
        form = BidForm(request.POST)
        if form.is_valid and float(request.POST.get("bid")) > auction.price:
            bid = request.POST.get("bid")
            new_bid = Bid(
                price=bid,
                date=timezone.now(),
                user=user,
                auction=auction
            )
            new_bid.save()
            auction.price = bid
            auction.save()

            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/listing.html", listing_attrs(auction, request.user, bm=f"Your Bid Must Be More Than {auction.price}"))

    return HttpResponseRedirect(reverse("listing", args=[id]))
            

@login_required
def add_comment(request, id):
    if request.method == "POST":
        form = CommentForm(request.POST)
        auction = Auction.objects.get(id=id)
        user = User.objects.get(username=request.user)
        if form.is_valid:
            text = request.POST.get("comment")
            new_comment = Comment(
                text=text,
                date=timezone.now(),
                user=user,
                auction=auction
            )
            new_comment.save()
            return render(request, "auctions/listing.html", listing_attrs(auction, request.user))

        else:
            return render(request, "auctions/listing.html", listing_attrs(auction, request.user, cm="INVALID COMMEMT"))
            
    return HttpResponseRedirect(reverse("listing", args=[id]))


@login_required
def close_auction(request, id):
    if request.method == "POST":
        auction = Auction.objects.get(id=id)
        winner = Bid.objects.get(auction=auction, price=auction.price).user
        print(winner)
        auction.closed = True
        auction.winner = winner
        auction.save()
        return HttpResponseRedirect(reverse("index"))



@login_required
def watchlist(request):
    user = User.objects.get(username=request.user)
    listings = WatchList.objects.filter(user=user)
    return render(
        request,
        "auctions/watchlist.html",
        {
            "listings": [i.auction for i in listings]
        }
                 )


@login_required
def addto_wl(request, id):
    if request.method == "POST":
        user = User.objects.get(username=request.user)
        auction = Auction.objects.get(id=id)
        wl = WatchList(user=user, auction=auction)
        wl.save()
        return HttpResponseRedirect(reverse("watchlist"))


@login_required
def rm_wl(request, id):
    if request.method == "POST":
        user = User.objects.get(username=request.user)
        auction = Auction.objects.get(id=id)
        wl = WatchList.objects.get(user=user, auction=auction)
        wl.delete()
    return HttpResponseRedirect(reverse("watchlist"))


@login_required
def ctgs_view(request):
    ctgs = ["Others", "Technical", "Kitchen", "Animals", "Farm", "Kids"]
    return render(
        request,
        "auctions/categories.html",
        {
            "ctgs": ctgs
        }
                 )


@login_required
def ctg_filter(request, ctg):
    listings = Auction.objects.filter(category=ctg)
    return render(request, "auctions/ctgpage.html", {"listings": listings})
