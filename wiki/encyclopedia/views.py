from django.shortcuts import render

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "pagetitle": "Search Results"
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

def search(request):
    if request.method == "POST":
        searchquery = request.POST['q']
        content = util.get_entry(searchquery)
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
                return render(request, "encyclopedia/entry.html", {
                    "title": title,
                    "content": body
                })
            


    else:
        return render(request, "encyclopedia/createpage.html")

def editpage(request):
    if request.method == "POST":
        title = request.POST.get('edittitle')
        content = request.POST.get('editbody')
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
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": content
        })
    else:
        return render(request, "encyclopedia/error.html", {
            "message": "Error: GO FIND A PAGE TO EDIT FIRST"
        })