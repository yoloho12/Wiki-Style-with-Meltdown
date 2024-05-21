from django.shortcuts import render
from django import forms
from . import util
from django.urls import reverse
from django.http import HttpResponseRedirect
from random import randint
from markdown2 import markdown


class titleForm(forms.Form):
    title = forms.CharField(label="")


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form": titleForm()
    })


def wiki(request, title):
    entry = util.get_entry(title)
    if entry is None:
        return render(request, "encyclopedia/entry.html", {
            "entry": entry
        })
    return render(request, "encyclopedia/entry.html", {
        "entry": markdown(entry),
        "title": title,
        "form": titleForm()
    })


def search(request):
    if request.method == "GET":
        form = titleForm(request.GET)
        if form.is_valid():
            title = form.cleaned_data["title"]
            if util.get_entry(title) is not None:
                return wiki(request, title)
            titles = util.list_entries()
            similar_list = []
            for t in titles:
                if t[:len(title)].lower() == title[:len(title)].lower():
                    similar_list.append(t)
            if similar_list.__len__() != 0:
                return render(request, "encyclopedia/index.html", {
                    "entries": similar_list,
                    "form": titleForm()
                })
            else:
                title = None
                return wiki(request, title)
    return HttpResponseRedirect(reverse("index"))


class contentForm(forms.Form):
    title = forms.CharField(label="Title ")
    content = forms.CharField(widget=forms.Textarea())
    content.label = ''


def create(request):
    if request.method == "GET":
        return render(request, "encyclopedia/create.html", {
            "contentForm": contentForm
        })
    if request.method == "POST":
        data = contentForm(request.POST)
        if data.is_valid():
            title = data.cleaned_data["title"]
            content = data.cleaned_data["content"]
            if util.get_entry(title) is not None:
                return render(request, "encyclopedia/create.html", {
                    "contentForm": data,
                    "error": "Name has already exists!"
                })
            if title and content:
                util.save_entry(title, content)
                return wiki(request,title)
    return HttpResponseRedirect(reverse("create"))


def randompage(request):
    entries = util.list_entries()
    title = entries[randint(0, entries.__len__() - 1)]
    return wiki(request, title)


def edit(request):
    if request.method == 'POST':
        data = contentForm(request.POST)
        if data.is_valid():
            title = data.cleaned_data['title']
            content = data.cleaned_data['content']
            if title and content:
                util.save_entry(title, content)
        return wiki(request, title)
    else:
        data = titleForm(request.GET)
        if data.is_valid():
            title = data.cleaned_data["title"]
            content = util.get_entry(title)
            if not content or not title:
                return HttpResponseRedirect(reverse('index'))
        saveForm = contentForm(initial={'title': title, 'content': content})
        saveForm.fields['title'].widget = forms.HiddenInput()
        return render(request, "encyclopedia/edit.html", {
            "saveForm": saveForm,
            "title": title
        })
