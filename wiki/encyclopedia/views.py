from django.shortcuts import render

from . import util

import random
from markdown2 import Markdown


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "pagetitle": "Search Results"
    })

def viewentry(request, title):

    content = MarkdownConverter(title)
    if content == None:
        return render(request, "encyclopedia/error.html", {
            "message": "Error: No Entry Found"
        }) 

    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "content": content
    }) 

def search(request):
    if request.method == "POST":
        searchquery = request.POST['q']
        content = MarkdownConverter(searchquery)
        if content == None:
            searchresults = []
            allentries = util.list_entries()
            for entry in allentries:
                    if searchquery.lower() in entry.lower():
                        searchresults.append(entry)
            return render(request, "encyclopedia/index.html", {
                "entries": searchresults,
                "pagetitle": "Search Results"
            })
        else:
            return render(request, "encyclopedia/entry.html", {
                "title": searchquery,
                "content": content
            }) 

    else: 
        pass


def createpage(request):
    if request.method == "POST":
        if not request.POST['title']:
            return render(request, "encyclopedia/error.html", {
                "message": "Error: New Page Must Have a Title"
            }) 
        if not request.POST['body']:
            return render(request, "encyclopedia/error.html", {
                "message": "Error: New Page Must Have a Body"
            }) 
        else:
            title = request.POST['title']
            body = request.POST['body']
            allentries = util.list_entries()
            for entry in allentries:
                if title.lower() ==  entry.lower():
                    return render(request, "encyclopedia/error.html", {
                        "message": "Error: Entry Exists of The Same Title"
                    }) 
            else:
                util.save_entry(title, body)
                content = MarkdownConverter(title)
                return render(request, "encyclopedia/entry.html", {
                    "title": title,
                    "content": content
                })
    else:
        return render(request, "encyclopedia/createpage.html")

def editpage(request):
    if request.method == "POST":
        title = request.POST.get('edittitle')
        content = util.get_entry(title)
        return render(request, "encyclopedia/editpage.html", {
            "title": title,
            "content": content
        })
    else:
        return render(request, "encyclopedia/error.html", {
            "message": "Error: GO FIND A PAGE TO EDIT FIRST"
        })

def saveedit(request):
    if request.method == "POST":
        title = request.POST.get('edittitle')
        content = request.POST.get('editcontent')
        util.save_entry(title, content)
        content = MarkdownConverter(title)
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": content
        })
    else:
        return render(request, "encyclopedia/error.html", {
            "message": "Error: GO FIND A PAGE TO EDIT FIRST"
        })

def rand(request):
    allEntries= util.list_entries()

    randtitle = random.choice(allEntries)
    content = MarkdownConverter(randtitle)
    return render(request, "encyclopedia/entry.html", {
        "title": randtitle,
        "content": content
    })

def MarkdownConverter(title):
    markdowntext = util.get_entry(title)
    markdowner = Markdown()
    if markdowntext == None: 
        return None
    else:
        return markdowner.convert(markdowntext)