from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from .models import Client, Calendar
from .forms import ClientForm, CalendarForm
import datetime

def home(request):
    # Your code to display reports (if any) goes here
    # Example:
    # reports = YourReportModel.objects.all()
    # return render(request, 'home.html', {'reports': reports})

    # #We are creating form in order to get all field in an automated way
    # #including the file for the installationManual
    # if request.method == 'POST':
    #     calForm = calendarForm(request.POST, request.FILES)
    #     if calForm.is_valid():
    #         calForm.save()
    #         return redirect('db')
    # else:
    #     calForm = calendarForm()

    #This part (until the final render of the page) is needed for keeping the reports info on display
    dateStart = datetime.datetime.now() - datetime.timedelta(days=2*365)
    dateEnd = datetime.datetime.now() - datetime.timedelta(days=(2*365)-30)
    days = 335

    report_list = calendar.objects.raw("SELECT * FROM test_ent_calendar WHERE ( (job_type = 'ERROR' OR job_type = 'INSTALLATION' OR job_type = 'REMAKE' OR job_type = 'SERVICE') AND (category = 'ALARM' OR category = 'FIRE' OR category = 'CCTV') ) AND (date >= %s AND date <= %s)", [dateStart,dateEnd])
    # Show 1 calendar entry per page
    paginator = Paginator(report_list, 1)

    #Getting the current page in order to move the next or previous
    page = request.GET.get('page')

    try:
        report = paginator.page(page)
        return render(request, 'home.html',{'report':report,})
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        report = paginator.page(1)
        return render(request, 'home.html',{'report':report,})
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        report = paginator.page(paginator.num_pages)
        return render(request, 'home.html',{'report':report,})
    except calendar.DoesNotExist:
        return redirect ('home')

    #was the starting line which is not needed i believe
    #return render(request, 'db.html',{'report':report,})

#This is here in case we need it and we find something
#faulty in the "installationManual" presentation

# def installationManualShow(request):

#     try:
#         return FileResponse(open('C:/Users/EES/projects/psarrosent/media/Installation Manuals/How_to_build_a_NAS_on_RPi4.pdf', 'rb'), content_type='application/pdf')
#     except FileNotFoundError:
#         raise Http404('not found')

#     return render(request,'template.html')
    
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

def insert_client(request):
    # Handle insert client logic here
    if request.method == "POST":
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('db')
    else:
        form = ClientForm()
  
    return render(request, 'insert_client.html', {'form': form})

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

def display_client(request, client_id):
    client = get_object_or_404(Client, pk=client_id)
    return render(request, 'display_client.html', {'client': client})

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

def display_calendar(request, calendar_id):
    calendar_entry = get_object_or_404(Calendar, pk=calendar_id)
    return render(request, 'display_calendar.html', {'calendar_entry': calendar_entry})

# Search Complete view for both client and calendar
def search_complete(request):
    if request.method == 'POST':
        search_params = request.POST.get('search_params')
        # You can define your search criteria for both client and calendar here
        clients = Client.objects.filter(
            # Define your client search criteria based on search_params
        )
        calendars = Calendar.objects.filter(
            # Define your calendar search criteria based on search_params
        )
        return render(request, 'search_complete.html', {'clients': clients, 'calendars': calendars})
    return render(request, 'search_complete.html')

# Insert Complete view for both client and calendar
def insert_complete(request):
    if request.method == 'POST':
        # Implement the logic to insert data for both client and calendar here
        pass

# Update Client Complete view
def update_client_complete(request, client_id):
    client = get_object_or_404(Client, id=client_id)
    if request.method == 'POST':
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            return redirect('search_client')

    return render(request, 'update_client_complete.html', {'form': form, 'client': client})

# Insert Calendar Complete view
def insert_calendar_complete(request, client_id):
    client = get_object_or_404(Client, id=client_id)
    if request.method == 'POST':
        form = CalendarForm(request.POST)
        if form.is_valid():
            calendar = form.save(commit=False)
            calendar.client = client
            calendar.save()
            return redirect('search_calendar')

    return render(request, 'insert_calendar_complete.html', {'form': form, 'client': client})

# Update Calendar Complete view
def update_calendar_complete(request, calendar_id):
    calendar = get_object_or_404(Calendar, id=calendar_id)
    if request.method == 'POST':
        form = CalendarForm(request.POST, instance=calendar)
        if form.is_valid():
            form.save()
            return redirect('search_calendar')

    return render(request, 'update_calendar_complete.html', {'form': form, 'calendar': calendar})

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
