# views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import calendar, client
from django.db.models import Q
import datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
#from .forms import CalendarForm  # Import your CalendarForm
#from .forms import ClientForm  # Import your ClientForm
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
        form_type = request.POST.get('form_type')

        if form_type == 'calendar':
            search_form = calendarForm(request.POST)
            if search_form.is_valid():
                args = {}
                for field, value in search_form.cleaned_data.items():
                    if value:
                        args[field] = value
                search = calendar.objects.filter(**args)
                return render(request, 'search_complete.html', {'search': search})

#extra code that might work                
#        if form_type == 'calendar':
#            search_form = calendarForm(request.POST)
#            if search_form.is_valid():
#                args = {key: value for key, value in search_form.cleaned_data.items() if value}
#                search_results = calendar.objects.filter(**args)
#                return render(request, 'search_complete.html', {'search_results': search_results})


        elif form_type == 'client':
            client_data = {key: request.POST[key] for key in ['id', 'surname', 'name', 'address', 'city', 'phone', 'email']}
            args = {key: value for key, value in client_data.items() if value}
            search_results = client.objects.filter(**args)
            return render(request, 'search_complete_client.html', {'search': search_results})

    else:
        search_form = calendarForm()
    return render(request, 'search_complete.html', {'search_form': search_form})

def insert_complete(request):
    if request.method == 'POST':
        form_type = request.POST.get('form_type')

        if form_type == 'calendar':
            cal_form = calendarForm(request.POST, request.FILES)
            if cal_form.is_valid():
                cal_instance = cal_form.save()
                return redirect('db')  # Redirect to a success page for calendar insertion
            else:
                return HttpResponse("Invalid calendar data")

        elif form_type == 'client':
            cl_form = clientForm(request.POST)
            if cl_form.is_valid():
                cl_instance = cl_form.save()
                return redirect('db')  # Redirect to a success page for client insertion
            else:
                return HttpResponse("Invalid client data")

    else:
        cal_form = calendarForm(instance=cal_instance)
        cl_form = clientForm(instance=cl_instance)

    return HttpResponse("Invalid request")  # Return a response for GET requests or other cases

def update_complete(request, id):
    cal_instance = get_object_or_404(calendar, id=id)
    cl_instance, created = client.objects.get_or_create(email=cal_instance.email)

    if request.method == 'POST':
        form_type = request.POST.get('form_type')

        if form_type == 'calendar':
            cal_form = calendarForm(request.POST, request.FILES, instance=cal_instance)
            if cal_form.is_valid():
                cal_instance = cal_form.save()
                return redirect('db') # Redirect to a success page for client insertion
            else:
                return HttpResponse("Invalid calendar data")

        elif form_type == 'client':
            cl_form = clientForm(request.POST, instance=cl_instance)
            if cl_form.is_valid():
                cl_instance = cl_form.save()
                return redirect('db') # Redirect to a success page for client insertion
            else:
                return HttpResponse("Invalid client data")

        else:
            return HttpResponse("Wrong Form Type")

    else:
        cal_form = calendarForm(instance=cal_instance)
        cl_form = clientForm(instance=cl_instance)

    return HttpResponse("Invalid request")  # Return a response for GET requests or other cases

def client_search(request):
    if request.method == 'POST':
        # Retrieve the search query from the form
        search_query = request.POST.get('search_query')

        # Query the clients based on partial matches on all attributes
        clients = client.objects.filter(
            Q(surname__icontains=search_query) |
            Q(name__icontains=search_query) |
            Q(address__icontains=search_query) |
            Q(city__icontains=search_query) |
            Q(phone__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(comments__icontains=search_query)
        )

        return render(request, 'client_search.html', {'clients': clients})
    else:
        return render(request, 'client_search.html', {'clients': None})

def add(request):

    val1 = int(request.POST['num1'])
    val2 = int(request.POST['num2'])
    rs = val1+val2

    return render(request, 'result.html', {'result':rs})

def about(request):
    return render(request, 'about.html')

def products(request):
    return render(request, 'products.html')

def contact(request):
    return render(request, 'contact.html')
