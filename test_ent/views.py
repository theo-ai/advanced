# views.py

from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Calendar, Client
from django.db.models import Q
import datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import CalendarForm  # Import your CalendarForm
from .forms import ClientForm  # Import your ClientForm
from .forms import calendarForm, clientForm

def home(request):
    return render(request, 'home.html', {'name': 'theo'})

def login(request):
    pass

def db(request):
    date_start = datetime.datetime.now() - datetime.timedelta(days=2 * 365)
    date_end = datetime.datetime.now() - datetime.timedelta(days=(2 * 365) - 30)

    report_list = calendar.objects.filter(
        Q(job_type__in=['ERROR', 'INSTALLATION', 'REMAKE', 'SERVICE']) &
        Q(category__in=['ALARM', 'FIRE', 'CCTV']) &
        Q(date__range=[date_start, date_end])
    ).order_by('date')

    paginator = Paginator(report_list, 1)
    page = request.GET.get('page')

    try:
        report = paginator.page(page)
    except PageNotAnInteger:
        report = paginator.page(1)
    except EmptyPage:
        report = paginator.page(paginator.num_pages)

    return render(request, 'db.html', {'report': report})

def search_complete(request):
    if request.method == 'POST':
        search_form = calendarForm(request.POST)
        if search_form.is_valid():
            args = {}
            for field, value in search_form.cleaned_data.items():
                if value:
                    args[field] = value
            search_results = calendar.objects.filter(**args)
            return render(request, 'search_complete.html', {'search_results': search_results})
    else:
        search_form = calendarForm()
    return render(request, 'search_complete.html', {'search_form': search_form})

def insert_complete(request):
    if request.method == 'POST':
        cal_form = calendarForm(request.POST, request.FILES)
        cl_form = clientForm(request.POST)
        if cal_form.is_valid() and cl_form.is_valid():
            cal_instance = cal_form.save()
            cl_instance, created = client.objects.get_or_create(email=cal_instance.email)
            cl_form = clientForm(request.POST, instance=cl_instance)
            if cl_form.is_valid():
                cl_form.save()
            return redirect('db')
    else:
        cal_form = calendarForm()
        cl_form = clientForm()
    return render(request, 'insert_complete.html', {'cal_form': cal_form, 'cl_form': cl_form})

def update_complete(request, id):
    cal_instance = get_object_or_404(calendar, id=id)
    cl_instance, created = client.objects.get_or_create(email=cal_instance.email)

    if request.method == 'POST':
        cal_form = calendarForm(request.POST, request.FILES, instance=cal_instance)
        cl_form = clientForm(request.POST, instance=cl_instance)
        if cal_form.is_valid() and cl_form.is_valid():
            cal_form.save()
            cl_form.save()
            return redirect('db')
    else:
        cal_form = calendarForm(instance=cal_instance)
        cl_form = clientForm(instance=cl_instance)

    return render(request, 'update_complete.html', {'cal_form': cal_form, 'cl_form': cl_form})

# Add more views as needed...

def about(request):
    return render(request, 'about.html')

def products(request):
    return render(request, 'products.html')

def contact(request):
    return render(request, 'contact.html')
