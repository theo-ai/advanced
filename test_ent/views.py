from django.shortcuts import render
from django.http import HttpResponse
from .models import calendar, client
from django.db.models import Q
import datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.

def home(request):
    return render(request, 'home.html',{'name':'theo'})

def login(request):
    pass

def db(request):

    dateStart = datetime.datetime.now() - datetime.timedelta(days=2*365)
    dateEnd = datetime.datetime.now() - datetime.timedelta(days=(1*365)-30)
    days = 335

    search_list = calendar.objects.raw("SELECT * FROM test_ent_calendar WHERE ( (job_type = 'ERROR' OR job_type = 'INSTALLATION' OR job_type = 'REMAKE') AND (category = 'ALARM' OR category = 'FIRE' OR category = 'CCTV') ) AND (date >= %s AND date <= %s)", [dateStart,dateEnd])
    # Show 1 calendar entry per page
    paginator = Paginator(search_list, 1) 

    #Getting the current page in order to move the next or previous
    page = request.GET.get('page')

    try:
        search = paginator.page(page)
        return render(request, 'db.html',{'report':search})
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        search = paginator.page(1)
        return render(request, 'db.html',{'report':search})
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        search = paginator.page(paginator.num_pages)
        return render(request, 'db.html',{'report':search})
    except calendar.DoesNotExist:
        return redirect ('db')


    return render(request, 'db.html',{'report':search})

#This is here in case we need it and we find something
#faulty in the "installationManual" presentation 

# def installationManualShow(request):

#     try:
#         return FileResponse(open('C:/Users/EES/projects/psarrosent/media/Installation Manuals/How_to_build_a_NAS_on_RPi4.pdf', 'rb'), content_type='application/pdf')
#     except FileNotFoundError:
#         raise Http404('not found')

#     return render(request,'template.html')

def search_complete(request):

    id = request.POST['id']
    date_temp = request.POST['date']
    #converting string "date_temp" to datetime "date"
    if date_temp != "":
        date = datetime.datetime.strptime(date_temp, '%Y/%m/%d')
    else:
        date = None
    surname = request.POST['surname']
    name = request.POST['name']
    address = request.POST['address']
    city = request.POST['city']
    phone = request.POST['phone']
    email = request.POST['email']
    job_type = request.POST['job_type']
    category = request.POST['category']

    print(id,date,surname,name,address,city,phone,email,job_type,category)

    args = [id,date,surname,name,address,city,phone,email,job_type,category]

    try:
        #needs fixing
        search = calendar.objects.filter(job_type=job_type)
    except calendar.DoesNotExist:
        return render(request, 'db.html')
    # except calendar.AttributeError:
    #     return render(request, 'db.html')

    # print(search.date,search.surname,search.name,search.address,search.city,
    #     search.phone,search.email,search.job_type,search.category)

    return render(request, 'search_complete.html', {'search':search})

def insert_complete(request):

    #getting the input from insert page
    #and we are entering it to the database

    #first we create the calendar item to hold the calendar input
    cal = calendar()
    
    cal.date = request.POST['date']
    cal.surname = request.POST['surname']
    cal.name = request.POST['name']
    cal.address = request.POST['address']
    cal.city = request.POST['city']
    cal.phone = request.POST['phone']
    cal.email = request.POST['email']
    cal.job_type = request.POST['job_type']
    cal.category = request.POST['category']
    cal.file = request.POST['file']

    print(cal.file)

    cal.save(force_insert=True)

    #after we finish the calendar insert we check if the client 
    #already exists or not and in the first case we need to 
    #create the new client

    cl = client()

    cl.surname = request.POST['surname']
    cl = request.POST['name']
    cl.address = request.POST['address']
    cl.city = request.POST['city']
    cl.phone = request.POST['phone']
    cl.email = request.POST['email']


    if client.objects.filter(surname=cl.surname,name=cl.name,address=cl.address,
    city=cl.city,phone=cl.phone,email=cl.email).exists():
        pass
    else:
        cl.save(force_insert=True)


    # print(search.date,search.surname,search.name,search.address,search.city,
    #     search.phone,search.job_type,search.category)

    return render(request, 'db.html', {'name':'Theo'})

def update_complete(request):

    # we search the tuple in database with the id provided
    # and then we update the rest of the values
    id = request.POST['id']

    date = request.POST['date']
    surname = request.POST['surname']
    name = request.POST['name']
    address = request.POST['address']
    city = request.POST['city']
    phone = request.POST['phone']
    email = request.POST['email']
    job_type = request.POST['job_type']
    category = request.POST['category']
    manual = request.POST['file']

    #we need to update the rest of the values too
    calendar.objects.filter(id=id).update(date=date,surname=surname,name=name,addres=address,city=city,phone=phone,email=emai,job_type=job_type,category=category,file=manual)

    return render(request, 'db.html', {'name':'Theo'})

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