from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse
from rango.models import Category, Page
from rango.forms import Categoryform, PageForm, UserForm, UserProfileForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


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
        context_dict['category_name_url'] = category_name_url
    except Category.DoesNotExist:
        pass
    return render(request, 'rango/category.html', context_dict)


@login_required
def add_category(request):
    if request.method == "POST":
        form = Categoryform(request.POST)

        if form.is_valid():
            form.save(commit=True)
            return redirect(index)
        else:
            print(form.errors)
    else:
        form = Categoryform()
    return render(request, 'rango/add_category.html', {'form': form})


@login_required
def add_page(request, category_name_url):
    category_name = encode_url(category_name_url)
    if request.method == "POST":
        form = PageForm(request.POST)

        if form.is_valid():
            page = form.save(commit=False)
            cat = Category.objects.get(name=category_name)
            page.category = cat
            page.views = 0
            page.save()
            return category(request, category_name_url)
        else:
            print(form.errors)
    else:
        form = PageForm()
    return render(request, 'rango/add_page.html', {
        'category_name_url': category_name_url,
        'category_name': category_name,
        'form': form
    })


def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
            profile.save()
            registered = True
        else:
            print(user_form.errors, profile_form.errors) 
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
    return render(request, 'rango/register.html', {
        'user_form': user_form, 'profile_form': profile_form, 'registered': registered
    })


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                return HttpResponse("Your rango account is disabled")
        else:
            print("Invalid login details: {0}, {1}".format(username, password))
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, 'rango/login.html', {})


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')


def encode_url(category_name_url):
    return category_name_url.replace('_', ' ')


def decode_url(category_name):
    return category_name.replace(' ', '_')
