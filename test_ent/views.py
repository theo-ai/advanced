from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from .models import Client, Calendar
from .forms import ClientForm, CalendarForm

def home(request):
    # Your code to display reports (if any) goes here
    # Example:
    # reports = YourReportModel.objects.all()
    # return render(request, 'home.html', {'reports': reports})
    return render(request, 'home.html')

def search_client(request):
    query = request.GET.get('q')
    clients = Client.objects.filter(
        Q(surname__icontains=query) |
        Q(name__icontains=query) |
        Q(address__icontains=query) |
        Q(city__icontains=query) |
        Q(phone__icontains=query) |
        Q(email__icontains=query) |
        Q(comments__icontains=query)
    )

    return render(request, 'search_client.html', {'clients': clients, 'query': query})

def search_calendar(request):
    query = request.GET.get('q')
    results = Calendar.objects.filter(
        Q(client__surname__icontains=query) |
        Q(client__name__icontains=query) |
        Q(client__address__icontains=query) |
        Q(client__city__icontains=query) |
        Q(client__phone__icontains=query) |
        Q(client__email__icontains=query) |
        Q(client__comments__icontains=query) |
        Q(job_type__icontains=query) |
        Q(category__icontains=query) |
        Q(comments__icontains=query)
    )

    return render(request, 'search_calendar.html', {'results': results, 'query': query})

def insert_calendar(request, client_id):
    client = get_object_or_404(Client, pk=client_id)

    if request.method == 'POST':
        form = CalendarForm(request.POST, request.FILES)
        if form.is_valid():
            calendar_entry = form.save(commit=False)
            calendar_entry.client = client
            calendar_entry.save()
            return redirect('db')
    else:
        form = CalendarForm()

    return render(request, 'insert_calendar.html', {'form': form, 'client': client})

def insert_client(request):
    # Handle insert client logic here
    if request.method == "POST":
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse("Client added successfully.")
    else:
        form = ClientForm()
  
    return render(request, 'insert_client.html', {'form': form})

def display_client(request, client_id):
    client = get_object_or_404(Client, pk=client_id)
    return render(request, 'display_client.html', {'client': client})

def update_client(request, client_id):
    client = get_object_or_404(Client, pk=client_id)

    if request.method == 'POST':
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            return redirect('db')
    else:
        form = ClientForm(instance=client)

    return render(request, 'update_client.html', {'form': form, 'client': client})

def display_calendar(request, calendar_id):
    calendar_entry = get_object_or_404(Calendar, pk=calendar_id)
    return render(request, 'display_calendar.html', {'calendar_entry': calendar_entry})

def update_calendar(request, calendar_id):
    calendar_entry = get_object_or_404(Calendar, pk=calendar_id)

    if request.method == 'POST':
        form = CalendarForm(request.POST, instance=calendar_entry)
        if form.is_valid():
            form.save()
            return redirect('db')
    else:
        form = CalendarForm(instance=calendar_entry)

    return render(request, 'update_calendar.html', {'form': form, 'calendar_entry': calendar_entry})

def db(request):
    if request.method == 'POST':
        form_type = request.POST.get('form_type')
        if form_type == 'client':
            query = request.POST.get('q')
            clients = Client.objects.filter(
                Q(surname__icontains=query) |
                Q(name__icontains=query) |
                Q(address__icontains=query) |
                Q(city__icontains=query) |
                Q(phone__icontains=query) |
                Q(email__icontains=query) |
                Q(comments__icontains=query)
            )

            return render(request, 'search_client.html', {'clients': clients, 'query': query})
        elif form_type == 'calendar':
            query = request.POST.get('q')
            results = Calendar.objects.filter(
                Q(client__surname__icontains=query) |
                Q(client__name__icontains=query) |
                Q(client__address__icontains=query) |
                Q(client__city__icontains=query) |
                Q(client__phone__icontains=query) |
                Q(client__email__icontains=query) |
                Q(client__comments__icontains=query) |
                Q(job_type__icontains=query) |
                Q(category__icontains=query) |
                Q(comments__icontains=query)
            )

            return render(request, 'search_calendar.html', {'results': results, 'query': query})
    else:
        return render(request, 'db.html')
