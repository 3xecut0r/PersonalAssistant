from django.shortcuts import render, redirect, get_object_or_404
from .forms import ContactForm
from django.shortcuts import render
from datetime import date, timedelta
from .models import Contact
from .forms import ContactDeleteForm


def start_page(request):
    context = {}
    return render(request, 'Contacts/base.html', context)

  
def card_subtitle_view(request):
    return render(request, 'Contacts/card_subtitle.html')

#добавление контактов 
def add_contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('contact_list')  # Перенаправление на страницу со списком контактов
    else:
        form = ContactForm()
    return render(request, 'contacts/add_contact.html', {'form': form})


#поиск контактов среди контактов книги
def contact_search(request):
    query = request.GET.get('q')  # Получение поискового запроса из URL

    if query:
        # Если есть поисковый запрос, выполните поиск в модели Contact
        results = Contact.objects.filter(name__icontains=query)
    else:
        results = []

    context = {
        'query': query,
        'results': results,
    }
    return render(request, 'contacts/contact_search.html', context)


# редактирование контактов
def edit_contact(request, contact_id):
    contact = get_object_or_404(Contact, id=contact_id)

    if request.method == 'POST':
        form = ContactForm(request.POST, instance=contact)
        if form.is_valid():
            form.save()
            return redirect('contact_list')  # Перенаправление на страницу со списком контактов
    else:
        form = ContactForm(instance=contact)

    return render(request, 'contacts/edit_contact.html', {'form': form})


def delete_contact(request, contact_id):
    contact = get_object_or_404(Contact, id=contact_id)

    if request.method == 'POST':
        form = ContactDeleteForm(request.POST)
        if form.is_valid():
            contact.delete()
            return redirect('contact_list')  # Перенаправление на страницу со списком контактов
    else:
        form = ContactDeleteForm()

    return render(request, 'contacts/delete_contact.html', {'contact': contact, 'form': form})


# список всех контактов из базы данных
# def contact_list(request):
    
#     contacts = Contact.objects.all()

#     context = {
#         'contacts': contacts,
#     }

#     return render(request, 'contacts/contact_list.html', context)



def contact_list(request):
    contacts = Contact.objects.all()

    for contact in contacts:
        contact.days_until_birthday = days_until_birthday(contact.birthday)

    context = {
        'contacts': contacts,
    }

    return render(request, 'contacts/contact_list.html', context)





def days_until_birthday(birthday):
    today = date.today()
    next_birthday = birthday.replace(year=today.year)
    if today > next_birthday:
        next_birthday = next_birthday.replace(year=today.year + 1)
    days_left = (next_birthday - today).days
    return days_left

