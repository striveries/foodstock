from django.shortcuts import render

# Create your views here.
def show_main(request):
    context = {
        'name': 'Calista Sekar',
        'class': 'PBP C',
        'item_name' : 'wortel',
        'amount' : '2',

    }

    return render(request, "main.html", context)