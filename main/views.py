from django.http import HttpResponse
from django.core import serializers
from django.http import HttpResponseRedirect
from main.forms import ItemForm
from main.models import Items
from django.urls import reverse
from django.shortcuts import render
from django.shortcuts import get_object_or_404

# Create your views here.

def show_main(request):
    items = Items.objects.all()
    context = {
        'name': 'Calista Sekar',
        'class': 'PBP C',
        'items' : items,
        'count_item' : len(items)
    }

    return render(request, "main.html", context)

def create_item(request):
    form = ItemForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        form.save()
        return HttpResponseRedirect(reverse('main:show_main'))

    context = {'form': form}
    return render(request, "create_item.html", context)

def delete_item(request, item_id):
    # Get the item object to delete
    item = get_object_or_404(Items, pk=item_id)

    if request.method == 'POST':
        # Delete the item if the request method is POST
        item.delete()
        return HttpResponseRedirect(reverse('main:show_main'))

    # Render a confirmation page with a form to confirm deletion
    context = {'item': item}
    return render(request, 'delete_item.html', context)

# def show_html(request):
#     items = Items.objects.all()
#     context = {'items': items}
#     return render(request, "items.html", context)

def show_html(request):
    data = Items.objects.all()
    html_data = serializers.serialize("html", data)

    # Escape HTML tags and wrap in <pre> for formatting
    escaped_html = '<pre>' + html_data.replace('<', '&lt;').replace('>', '&gt;') + '</pre>'
    
    return HttpResponse(escaped_html, content_type="text/html")


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