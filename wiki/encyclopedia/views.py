from django.shortcuts import render

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def TITLE(request):
    return render(request, "encyclopedia/TITLE.html", {
        "entries": util.list_entries()
    })

