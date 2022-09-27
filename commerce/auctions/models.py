from tkinter import CASCADE
from turtle import title
from unicodedata import category
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
    price = models.FloatField()
    isActive =models.BooleanField(default=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="user")  # on_delete=models.CASCADE means that if the owner is deleted, listing/comments associated etc referencing the owner will be deleted 
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True, related_name="category")

    def __str__(self):
        return self.title