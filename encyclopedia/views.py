from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django import forms
from . import util
import re

import markdown2


class SearchForm(forms.Form):
    query = forms.CharField(label="Search Query")


def index(request):
    return render(request, "encyclopedia/index.html", {"entries": util.list_entries()})


def entry_page(request, title):
    if request.method == "POST":
        form = SearchForm(request.POST)
        query = form.cleaned_data["query"]
        return render(request, "encyclopedia/search.html", {"search": query})
    elif util.get_entry(title) == None:
        return render(request, "encyclopedia/error_page.html", {"title": title})
    else:
        return render(
            request,
            "encyclopedia/entry.html",
            {
                "title": title.capitalize(),
                "content": markdown2.markdown(util.get_entry(title)),
            },
        )


def new_entry(request):
    return render(request, "encyclopedia/new_entry.html")
