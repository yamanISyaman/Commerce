from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone


from .models import User, Auction, Bid, Comment
from .forms import CreateForm
from .util import is_valid_image

def index(request):
    return render(request, "auctions/index.html")


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


def create(request):
    if request.method == "POST":
        form = CreateForm(request.POST, request.FILES)
        
        if form.is_valid():
            data = form.cleaned_data
            user = User.objects.get(username=request.user)
            if is_valid_image(data["image"]):
                new_auction = Auction(
user=user,
title=data["title"], price=data["price"], description=data["description"], image=data["image"],
date=timezone.now()
                )
                new_auction.save()
                return HttpResponseRedirect(reverse("index"))
            else:
                return render(request, "auctions/create.html", {
                "form": CreateForm(),
                "message": "Invalid Image URL"
            })
        else:
            return render(request, "auctions/create.html", {
                "form": CreateForm(),
                "message": "Invalid Data"
            })
        
    else:
        return render(request, "auctions/create.html", {"form": CreateForm()})
        