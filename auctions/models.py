from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    username = models.CharField(max_length=100, unique=True, primary_key=True)
    email = models.EmailField(max_length=256)
    password = models.CharField(max_length=18)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ["email", "password"]

class Category(models.Model):
    category = models.CharField(max_length=1000)
    def __str__(self):
        return f"{self.category}"

class Comment(models.Model):
    user_comment = models.TextField(max_length=10000, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user}'s comment"

class Listing(models.Model):
    title= models.CharField(max_length = 1000, blank=True, null=True)
    image= models.FileField(upload_to='listing_images/')
    user= models.ForeignKey(User, on_delete=models.CASCADE, related_name="author")
    post_date = models.DateField(null=True, blank=True)
    expire_date = models.DateField(null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="type")
    highest_bid= models.DecimalField(max_digits=8, decimal_places=2)
    highest_bidder = models.ForeignKey(User, on_delete=models.PROTECT, related_name="best_customer")
    comments = models.ManyToManyField(Comment)
    description = models.TextField(max_length=1000, null=True, blank=True)

    def __str__(self):
        return f"{self.title}"

class Watchlist(models.Model):
    listings = models.ManyToManyField(Listing)
    user = models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user}'s Watchlist"