from ast import If
from pickle import NONE
from turtle import title
from django.shortcuts import render

from markdown2 import Markdown
import random

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def Markdown_to_HTML_Conversion(title):
    original = util.get_entry(title)
    markdowner = Markdown()
    if original == None:   #This if statement will mean only entries that exist are subjected to the conversion from markdown to HTML 
        return None
    else:
        return markdowner.convert(original)

def entry(request, title):
    entry = Markdown_to_HTML_Conversion(title)
    if entry == None:
        return render(request, "encyclopedia/error_message.html")
    else:
        return render(request, "encyclopedia/entry.html", {
            "title":title,
            "display": entry 
        })   


def search(request):
    if request.method == "POST":
        entry_search = request.POST['q']
        entry = Markdown_to_HTML_Conversion(entry_search)
        if entry is not None:
            return render(request, "encyclopedia/entry.html", {
                "title":entry_search,
                "display": entry 
            })   
        else:
            allEntries = util.list_entries()
            recommendation = []
            for entry in allEntries:
                if entry_search.lower() in entry.lower():
                    recommendation.append(entry)
            return render(request, "encyclopedia/search.html", {
                "recommendation": recommendation
            })

def new_page(request):
    if request.method == "GET":
        return render(request, "encyclopedia/new.html")
    else:
        title = request.POST['title']
        content = request.POST['content']
        titleExist = util.get_entry(title)
        if titleExist is not None:
            return render(request, "encyclopedia/error_message.html", {
                "message": "Entry page already exists"
            })
        else:
            util.save_entry(title, content)
            html_content = Markdown_to_HTML_Conversion(title)
            return render(request, "encyclopedia/entry.html", {
                "title": title,
                "display": html_content
            })

def edit(request):
    if request.method == "POST":
        title = request.POST['entry_title']
        content = util.get_entry(title)
        return render(request, "encyclopedia/edit.html", {
            "title": title,
            "content": content
        })


def save_edit(request):
    if request.method == "POST":
        title = request.POST['title']
        content = request.POST['content']
        util.save_entry(title, content)
        html_content = Markdown_to_HTML_Conversion(title)
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "display": html_content
        })

def rand(request):
    allEntries= util.list_entries()
    rand_entry = random.choice(allEntries)
    html_content = Markdown_to_HTML_Conversion(rand_entry)
    return render(request, "encyclopedia/entry.html", {
        "title": rand_entry,
        "display": html_content
    })