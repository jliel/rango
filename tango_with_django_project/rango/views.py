from django.shortcuts import render
# from django.http import HttpResponse
from rango.models import Category, Page


def index(request):
    # return HttpResponse("""Rango says Hello world
    # <br><p><a href="about/">About</a></p>""")
    # context_dict = { 'boldmessage':"I am bold font from the context" }
    category_list = Category.objects.all().order_by('-likes')[:5]
    pages = Page.objects.all().order_by('-views')[:5]
    for category in category_list:
        category.url = category.name.replace(' ', '_')
    return render(request, 'rango/index.html', {"categories": category_list,
                                                "pages": pages})


def about(request):
    # return HttpResponse("""Rango Says: Here is the about page.
    # <br><p><a href="/rango">back</a></p>""")
    context_dict = { 'nab_message':"El we es nab" }
    return render(request, 'rango/about.html', context_dict)


def category(request, category_name_url):
    category_name = encode_url(category_name_url)
    context_dict = {'category_name': category_name}
    try:
        category = Category.objects.get(name=category_name)
        pages = Page.objects.all().filter(category=category)
        context_dict['pages'] = pages
        context_dict['category'] = category
    except Category.DoesNotExist:
        pass
    return render(request, 'rango/category.html', context_dict)


def encode_url(category_name_url):
    return category_name_url.replace('_', ' ')


def decode_url(category_name):
    return category_name.replace(' ', '_')
