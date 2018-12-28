from django.shortcuts import render
from django.http import HttpResponse


def index(request):
   # return HttpResponse("""Rango says Hello world
   # <br><p><a href="about/">About</a></p>""")
   context_dict = { 'boldmessage':"I am bold font from the context" }
   return render(request, 'rango/index.html', context_dict)

def about(request):
    # return HttpResponse("""Rango Says: Here is the about page.
    # <br><p><a href="/rango">back</a></p>""")
    context_dict = { 'nab_message':"El we es nab" }
    return render(request, 'rango/about.html', context_dict)
