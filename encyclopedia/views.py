from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
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
    if request.method == "GET":
        return render(request, "encyclopedia/new_entry.html")
    form_title = request.POST.get("entry_title")
    form_content = request.POST.get("entry_content")

    if util.get_entry(form_title):  # Might need to change to is not None
        return HttpResponseBadRequest("We already have a wiki page for this.")

    util.save_entry(form_title, form_content)
    return redirect(f"/wiki/{form_title}")
