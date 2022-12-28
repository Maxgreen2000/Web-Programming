from django.shortcuts import render

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def viewentry(request, title):

    content = util.get_entry(title)
    if content == None:
        return render(request, "encyclopedia/error.html", {
            "message": "Error: No Entry Found"
        }) 

    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "content": content
    }) 