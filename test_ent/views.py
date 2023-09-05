# views.py

from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import calendar, client
from django.db.models import Q
import datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import CalendarForm  # Import your CalendarForm
from .forms import ClientForm  # Import your ClientForm

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

def insert_complete(request):
    if request.method == 'POST':
        cal_form = CalendarForm(request.POST)
        if cal_form.is_valid():
            cal = cal_form.save(commit=False)
            cal.save()

            client_form = ClientForm(request.POST)
            if client_form.is_valid():
                client_obj, created = client.objects.get_or_create(
                    surname=cal.surname,
                    name=cal.name,
                    address=cal.address,
                    city=cal.city,
                    phone=cal.phone,
                    email=cal.email
                )
            return redirect('db')
    else:
        cal_form = CalendarForm()
        client_form = ClientForm()

    return render(request, 'insert_complete.html', {'cal_form': cal_form, 'client_form': client_form})

def search_complete(request):
    ident = request.POST.get('id')
    date_temp = request.POST.get('date')
    # Convert string "date_temp" to datetime "date"
    if date_temp:
        date = datetime.datetime.strptime(date_temp, '%Y/%m/%d')
    else:
        date = None

    # Similar code for other search parameters

    args = Q()
    if ident:
        args &= Q(id=ident)
    if date:
        args &= Q(date=date)
    # Add similar clauses for other search parameters

    try:
        search = calendar.objects.filter(args)
    except calendar.DoesNotExist:
        return render(request, 'db.html')

    return render(request, 'search_complete.html', {'search': search})

def update_complete(request):
    ident = request.POST.get('id')

    try:
        cal = calendar.objects.get(id=ident)

        # Update cal object with the provided data
        cal_form = CalendarForm(request.POST, instance=cal)
        if cal_form.is_valid():
            cal_form.save()

        # Update client object (if needed) with the provided data
        client_obj, created = client.objects.get_or_create(
            surname=cal.surname,
            name=cal.name,
            address=cal.address,
            city=cal.city,
            phone=cal.phone,
            email=cal.email
        )
        client_form = ClientForm(request.POST, instance=client_obj)
        if client_form.is_valid():
            client_form.save()

        return redirect('db')
    except calendar.DoesNotExist:
        return render(request, 'db.html')

# Other views (search_complete_client, insert_complete_client, update_complete_client, etc.) can be similarly refactored and optimized.
