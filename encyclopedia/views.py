from django.shortcuts import render
from . import util
import markdown,random,re


def index(request):
    context ={}
    if request.method == "POST":
        query = request.POST.get('query')
        if query in util.list_entries():
            return wiki(request,query)
        context['entries'] = []
        for entry in util.list_entries():
            if re.search(query.lower(),markdown.markdown(util.get_entry(entry)).lower()):
                context['entries'].append(entry)
        context['pages'] = f'Page(s) with {query}'
        return render(request, "encyclopedia/index.html", context)

    context["entries"] = util.list_entries()
    context['pages'] = 'All pages'
    return render(request, "encyclopedia/index.html", context)



def new(request):
    if request.method == "POST":
        title = request.POST.get('entry_title')
        if title not in util.list_entries():
            content = request.POST.get('entry_content')
            util.save_entry(title,content)
            return wiki(request,title)
        else:
            msg = f"Entry with title {title} already exists"
            title = "Already Exists"
        return render(request,"encyclopedia/404.html",{"message": msg, "title": title})
    return render(request, "encyclopedia/new.html")


def wiki(request,title):
    context = {}
    if title == 'random':
        context['title'] = random.choice(util.list_entries())
        context['raw_entry'] = util.get_entry(context['title'])
    else:
        context['title'] = title
        context['raw_entry'] = util.get_entry(title)

    try:
        context['entry'] = markdown.markdown(context['raw_entry'])
        return render(request,"encyclopedia/wiki.html",context)
    except:   
        msg = f"{context['title']} does not exist!!!"
        title = "Entry Not Found"
        return render(request,"encyclopedia/404.html",{"message": msg, "title": title})


def edit(request,title):
    context = {}
    context['title'] = title
    context['raw_entry'] = util.get_entry(title)
    if request.method == "POST":
        util.save_entry(title,request.POST.get('entry_content'))
        return wiki(request,context['title'])
    if context['raw_entry']:
        return render(request,"encyclopedia/edit.html",context)
    else:
        pass
