from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.urls import reverse
from django import forms
from . import util
import re
from django.contrib import messages

import markdown2
import random


class SearchForm(forms.Form):
    query = forms.CharField(label="Search Query")


def index(request):
    return render(request, "encyclopedia/index.html", {"entries": util.list_entries()})


def search(request):
    entries = util.list_entries()
    entries_low = [x.lower() for x in entries]
    query = request.GET.get("q")
    if query.lower() in entries_low:
        return redirect(f"/wiki/{query}")
    results = [entry for entry in entries if query.lower() in entry.lower()]
    # Note to self, this is saying include an entry in the results list if the query is a substring of it
    return render(request, "encyclopedia/index.html", {"entries": results})


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

def edit_page(request, title):
    return render(
        request, 
        "encyclopedia/edit.html",
        {
            "title":title.capitalize(), 
            "content": util.get_entry(title),
        },
    )

def new_entry(request):
    if request.method == "GET":
        return render(request, "encyclopedia/new_entry.html")
    form_title = request.POST.get("entry_title")
    form_content = request.POST.get("entry_content")

    if util.get_entry(form_title):
        # return HttpResponseBadRequest("We already have a wiki page for this.")
        messages.error(
            request,
            f"We already have a page for '{form_title}', why don't you make a page about something else.",
        )
        return redirect("new_entry")

    util.save_entry(form_title, form_content)
    return redirect(f"/wiki/{form_title}")

def random_page(request):
    return redirect(f"wiki/{random.choice(util.list_entries())}")
