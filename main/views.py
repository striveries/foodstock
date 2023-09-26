import datetime
from django.http import HttpResponse
from django.core import serializers
from django.http import HttpResponseRedirect
from main.forms import ItemForm
from main.models import Items
from django.urls import reverse
from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages  
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='/login')
def show_main(request):
    items = Items.objects.filter(user=request.user)
    context = {
        'name': request.user.username,
        'class': 'PBP C',
        'items' : items,
        'count_item' : len(items),
        'last_login': request.COOKIES['last_login'],
    }

    if 'add_success' in request.GET:
        context['add_success'] = True
    if 'reduce_success' in request.GET:
        context['reduce_success'] = True
    if 'delete_success' in request.GET:
        context['delete_success'] = True

    return render(request, "main.html", context)

def create_item(request):
    form = ItemForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        item = form.save(commit=False)
        item.user = request.user
        item.save()
        return HttpResponseRedirect(reverse('main:show_main'))

    context = {'form': form}
    return render(request, "create_item.html", context)

def show_xml(request):
    data = Items.objects.all()
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json(request):
    data = Items.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def show_xml_by_id(request, id):
    data = Items.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json_by_id(request, id):
    data = Items.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def register(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been successfully created!')
            return redirect('main:login')
    context = {'form':form}
    return render(request, 'register.html', context)

def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            response = HttpResponseRedirect(reverse("main:show_main")) 
            response.set_cookie('last_login', str(datetime.datetime.now()))
            return response
        else:
            messages.info(request, 'Sorry, incorrect username or password. Please try again.')
    context = {}
    return render(request, 'login.html', context)

def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('main:login'))
    response.delete_cookie('last_login')
    return response


def add_item(request, item_id):
    item = get_object_or_404(Items, pk=item_id)
    if request.method == 'POST':
        item.amount += 1
        item.save()
        return HttpResponseRedirect(reverse('main:show_main'))

    # Render a confirmation page with a form to confirm deletion
    context = {'item': item}
    return render(request, 'add_item.html', context)

def reduce_item(request, item_id):
    item = get_object_or_404(Items, pk=item_id)
    if request.method == 'POST':
        if item.amount > 0:
            item.amount -= 1
            item.save()
            return HttpResponseRedirect(reverse('main:show_main'))

    # Render a confirmation page with a form to confirm deletion
    context = {'item': item}
    return render(request, 'reduce_item.html', context)

def delete_item(request, item_id):
    # item = get_object_or_404(Items, pk=item_id)
    # item.delete()
    # return HttpResponseRedirect(reverse('main:show_main'))

    # Get the item object to delete
    item = get_object_or_404(Items, pk=item_id)

    if request.method == 'POST':
        # Delete the item if the request method is POST
        item.delete()
        return HttpResponseRedirect(reverse('main:show_main'))
    # Render a confirmation page with a form to confirm deletion
    context = {'item': item}
    return render(request, 'delete_item.html', context)