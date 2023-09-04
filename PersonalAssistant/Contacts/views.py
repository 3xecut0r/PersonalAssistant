from django.shortcuts import render, redirect, get_object_or_404
from .forms import ContactForm
from django.shortcuts import render
from datetime import date, timedelta
from .models import Contact

def add_contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('contact_list')  
    else:
        form = ContactForm()
    return render(request, 'contacts/add_contact.html', {'form': form})


def start_page(request):
    context = {}
    return render(request, 'Contacts/base.html', context)


def card_subtitle_view(request):
    return render(request, 'Contacts/card_subtitle.html')


def add_contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('contact_list')  # Перенаправление на страницу со списком контактов
    else:
        form = ContactForm()
    return render(request, 'contacts/add_contact.html', {'form': form})



# поиск контактов, у которых день рождения через заданное количество дней от текущей даты
def upcoming_birthdays(request, days=7):
    # Определение текущей даты
    today = date.today()

    # Определение дату через заданное количество дней
    future_date = today + timedelta(days=days)

    # Определение контактов, у которых дни рождения между текущей датой и будущей датой
    upcoming_contacts = Contact.objects.filter(
        birth_date__gte=today, birth_date__lte=future_date
    )

    context = {
        'upcoming_contacts': upcoming_contacts,
        'future_date': future_date,
    }

    return render(request, 'contacts/upcoming_birthdays.html', context)



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


# удаление контактов
def delete_contact(request, contact_id):
    contact = get_object_or_404(Contact, id=contact_id)

    if request.method == 'POST':
        contact.delete()
        return redirect('contact_list')  # Перенаправление на страницу со списком контактов

    return render(request, 'contacts/delete_contact.html', {'contact': contact})