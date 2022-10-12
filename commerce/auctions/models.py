from email import message
from email.policy import default
from tkinter import CASCADE
from turtle import title
from unicodedata import category
from unittest.util import _MAX_LENGTH
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    categoryName = models.CharField(max_length=100)

    def __str__(self):      #Displays category name now not category object [n]. 4 categories based of Car and Classic website and covers a whole general market.
        return self.categoryName

class Listing(models.Model):
    title = models.CharField(max_length=80)  #80 characters is Ebay's limit
    description = models.TextField(max_length=1000) #Ebay doesn't have a max length for descriptions in reality  /   CharField has a max of 255 characters thus use a textfield instead.
    imageUrl = models.TextField(max_length=500) #Need to be a massive length to accomadate very long urls
    startingPrice = models.FloatField(default=0)
    highestBid = models.FloatField(default=0)
    highestBidder = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="highestBidder")
    bidCounter = models.IntegerField(default=0)
    isActive =models.BooleanField(default=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="user")  # on_delete=models.CASCADE means that if the owner is deleted, listing/comments associated etc referencing the owner will be deleted 
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True, related_name="category")
    watchlist = models.ManyToManyField(User, blank=True, null=True, related_name="listingWatchlist")

    def __str__(self):
        return self.title

class Comment(models.Model):             #COMMENTS SHOULD ALSO HAVE A TIME 
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="userComment")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, blank=True, null=True, related_name="listingComment")
    message = models.CharField(max_length=250)

    def __str__(self):
        return f"{self.author} commented on {self.listing}"

