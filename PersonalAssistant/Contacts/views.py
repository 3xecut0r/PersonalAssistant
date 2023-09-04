from django.shortcuts import render

# Create your views here.


def start_page(request):
    context = {}
    return render(request, 'Contacts/base.html', context)
