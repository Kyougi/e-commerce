from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from datetime import datetime

from .models import User, Watchlist, Listing, Category, Comment


def index(request):
    allListings = Listing.objects.all()
    current_date = datetime.now()
    return render(request, "auctions/index.html", {
        "listings": allListings,
        "current_date": current_date
    })

def create_listing(request):
    if request.method == "POST":
        if not Listing.objects.filter(title=request.POST.get("title")).exists():
            new_listing = Listing.objects.create(title = request.POST.get("title"),
                                             image = request.FILES.get("image"),
                                             user = request.user,
                                             post_date = datetime.now(),
                                             expire_date = request.POST.get("date"),
                                             category = Category.objects.get(category=request.POST.get("category")),
                                             highest_bid = request.POST.get("price"),
                                             highest_bidder = request.user,
                                             description = request.POST.get("description"))
            new_listing.save()
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/create_listing.html",{
                "message": f"This listing already exists"
            })
    return render(request, "auctions/create_listing.html", {
        "categories": Category.objects.all()
    })


def listing(request, title):
    listing = Listing.objects.get(title=title)
    if request.method == "POST":
        new_bid = request.POST.get("bid")
        if request.user == listing.user:
            return render(request, "auctions/listing.html", {
                "message": "The author cannot bid their own auction after creation!"
            })
        else:
            new_bid = float(new_bid)
            if new_bid > listing.highest_bid:
                listing.highest_bid = new_bid
                listing.highest_bidder = request.user
                listing.save()
            else:
                return render(request, "auctions/listing.html", {
                "message": "Error: Your bid is lower than the current highest bid"
            })
    user_watchlist = Watchlist.objects.get(user=request.user)
    exists = False
    if user_watchlist.listings.filter(id=listing.id).exists():
        exists = True
    return render(request, "auctions/listing.html", {
        "listing": listing,
        "comments": listing.comments.all(),
        "exists": exists,
        "message": ""
    })



def comments(request, title):
    if request.method == "POST":
        a_comment = request.POST.get("comment")
        new_comment = Comment.objects.create(user_comment=a_comment,
                                             user=request.user)
        new_comment.save()
        existing_listing = Listing.objects.get(title=title)
        existing_listing.comments.add(new_comment)
        return HttpResponseRedirect(reverse("listing", args=[existing_listing.title]))

def addWatchlist(request, id):
    if request.method=="POST":
        user_watchlist = Watchlist.objects.get(user=request.user)
        existing_listing = Listing.objects.get(pk=id)
        user_watchlist.listings.add(existing_listing)
        user_watchlist.save()
        return HttpResponseRedirect(reverse("listing", args=[existing_listing.title]))

def removeWatchlist(request, id):
    if request.method=="POST":
        user_watchlist = Watchlist.objects.get(user=request.user)
        existing_listing = Listing.objects.get(pk=id)
        user_watchlist.listings.remove(existing_listing)
        user_watchlist.save()
        return HttpResponseRedirect(reverse("listing", args=[existing_listing.title]))

def category(request, category):
    cat = Category.objects.get(category=category)
    listings = Listing.objects.filter(category=cat)
    return render(request, "auctions/category.html", {
        "listings": listings,
        "category": category
    })

def watchlist(request):
    user_watchlist = Watchlist.objects.get(user=request.user)
    listings = user_watchlist.listings.all()
    return render(request, "auctions/watchlist.html", {
        "listings": listings,
        "user": request.user
    })

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
            new_user = User.objects.create_user(username, email, password)
            new_user.save()
            user_watchlist = Watchlist.objects.create(user=new_user)
            user_watchlist.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, new_user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
