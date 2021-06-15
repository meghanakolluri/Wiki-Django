import os
import markdown2


from django.shortcuts import render
from django import forms
from . import util
from django.http import HttpResponse, HttpResponseRedirect, request
from django.urls import reverse
from django.core.files import File
import random

class NewTaskForm(forms.Form):
    task1=forms.CharField(label="Title")
    task2=forms.CharField(label="Content",widget=forms.Textarea(attrs={'rows':'30','cols':'50'}))
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()} )
def new(request):
    if request.method=="POST":
        form=NewTaskForm(request.POST)
        if form.is_valid():
            task1=form.cleaned_data["task1"]
            task2=form.cleaned_data["task2"]
            if task1 not in util.list_entries():
                util.save_entry(task1,task2)
                return HttpResponseRedirect(reverse('encyclopedia:index'))
            else:
                return render(request,"encyclopedia/error2page.html")
        else:
            return render(request,"encyclopedia/new.html",{"form":form})
    return render(request,"encyclopedia/new.html",{"form":NewTaskForm()})
def entry_page(request,page):
    try:
        print(util.get_entry(page))
        mark,mybool=util.get_entry(page)
        htmlcontents = markdown2.markdown(mark)
     
        return render(request,"encyclopedia/entrypage.html",{
            "title":page,
            "html" : htmlcontents
        })
    except TypeError:
        return render(request,"encyclopedia/errorpage.html")

def editpage(request,title):
    md, mybool = util.get_entry(title)
    htmlcontents = markdown2.markdown(md)
    return render(request, "encyclopedia/editpage.html",{
        "title" : title,
        "mdcontent" : md
    })

def welcome(request):
    return render(request,"encyclopedia/welcome.html")


def edit(request):
    title = request.POST['title']
    textarea = request.POST['textarea']
    title=title.strip(' ')
    util.save_entry(title,textarea)   
    htmlcontents = markdown2.markdown(textarea)
    return render(request, "encyclopedia/entrypage.html",{
        "title" : title,
        "html" : htmlcontents
    })

def randompage(request):
    filename = random.choice(os.listdir(r"C:\Users\kollu\Downloads\wiki\wiki\entries"))
    title = os.path.splitext(filename)[0] 

    mdcontents, mybool = util.get_entry(title)
    html=markdown2.markdown(mdcontents)
    print(title)
    print(html)
    
    return render(request,"encyclopedia/entrypage.html",{
    "title":title,
    "html" : html
    })

def search(request):
    title=request.POST['q']
    entries=util.list_entries()
    r=[]
    for entry in entries:
        if entry.find(title)==-1:
            pass
        else:
            r.append(entry)
    if r:
        return render(request,"encyclopedia/result.html",{
            "results":r
        })
    else:
        return render(request,"encyclopedia/error1page.html")

