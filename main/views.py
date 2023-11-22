import datetime
import json
from django.http import HttpResponse, HttpResponseNotFound, JsonResponse
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
from django.views.decorators.csrf import csrf_exempt 


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

def user_page(request):
    items = Items.objects.filter(user=request.user)
    context = {
        'name': request.user.username,
        'class': 'PBP C',
    }

    return render(request, "user_page.html", context)

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

@csrf_exempt
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

@csrf_exempt
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


def add_item(request, id):
    item = Items.objects.get(pk = id)
    if item.amount > 0:
            item.amount += 1
            item.save()
            return HttpResponseRedirect(reverse('main:show_main'))
    # Kembali ke halaman awal
    return HttpResponseRedirect(reverse('main:show_main'))

def reduce_item(request, id):
    item = Items.objects.get(pk = id)
    if item.amount > 0:
            item.amount -= 1
            item.save()
            return HttpResponseRedirect(reverse('main:show_main'))
    # Kembali ke halaman awal
    return HttpResponseRedirect(reverse('main:show_main'))

def delete_item(request, id):
    # Get data berdasarkan ID
    item = Items.objects.get(pk = id)
    # Hapus data
    item.delete()
    # Kembali ke halaman awal
    return HttpResponseRedirect(reverse('main:show_main'))

def edit_item(request, id):
    # Get product berdasarkan ID
    item = Items.objects.get(pk = id)

    # Set product sebagai instance dari form
    form = ItemForm(request.POST or None, instance=item)

    if form.is_valid() and request.method == "POST":
        # Simpan form dan kembali ke halaman awal
        form.save()
        return HttpResponseRedirect(reverse('main:show_main'))

    context = {'form': form}
    return render(request, "edit_item.html", context)


def get_product_json(request):
    item = Items.objects.filter(user=request.user)
    return HttpResponse(serializers.serialize('json', item))


@csrf_exempt
def add_item_ajax(request):
    if request.method == 'POST':
        name = request.POST.get("item_name")
        amount = request.POST.get("amount")
        description = request.POST.get("description")
        user = request.user

        new_product = Items(item_name=name, amount=amount, description=description, user=user)
        new_product.save()

        return HttpResponse(b"CREATED", status=201)

    return HttpResponseNotFound()


@csrf_exempt
def create_product_flutter(request):
    if request.method == 'POST':
        
        data = json.loads(request.body)

        new_product = Items.objects.create(
            user = request.user,
            name = data["name"],
            price = int(data["price"]),
            description = data["description"]
        )

        new_product.save()

        return JsonResponse({"status": "success"}, status=200)
    else:
        return JsonResponse({"status": "error"}, status=401)