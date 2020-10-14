from django.shortcuts import render, redirect
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
    dateEnd = datetime.datetime.now() - datetime.timedelta(days=(1*365)-30)
    days = 335

    report_list = calendar.objects.raw("SELECT * FROM test_ent_calendar WHERE ( (job_type = 'ERROR' OR job_type = 'INSTALLATION' OR job_type = 'REMAKE') AND (category = 'ALARM' OR category = 'FIRE' OR category = 'CCTV') ) AND (date >= %s AND date <= %s)", [dateStart,dateEnd])
    # Show 1 calendar entry per page
    paginator = Paginator(report_list, 1) 

    #Getting the current page in order to move the next or previous
    page = request.GET.get('page')

    try:
        report = paginator.page(page)
        return render(request, 'db.html',{'report':report,})
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        report = paginator.page(1)
        return render(request, 'db.html',{'report':report,})
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        report = paginator.page(paginator.num_pages)
        return render(request, 'db.html',{'report':report,})
    except calendar.DoesNotExist:
        return redirect ('db')


    return render(request, 'db.html',{'report':report,})

#This is here in case we need it and we find something
#faulty in the "installationManual" presentation 

# def installationManualShow(request):

#     try:
#         return FileResponse(open('C:/Users/EES/projects/psarrosent/media/Installation Manuals/How_to_build_a_NAS_on_RPi4.pdf', 'rb'), content_type='application/pdf')
#     except FileNotFoundError:
#         raise Http404('not found')

#     return render(request,'template.html')

def search_complete(request):

    ident = request.POST['id']
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

    #Gathering all the given search parameters in order to search only for them
    args = Q()
    if surname != '':
        args = args & Q(surname=surname)
    if phone != '':
        args = args & Q(phone=phone)
    if date != None:
        args = args & Q(date=date)
    if name != '':
        args = args & Q(name=name)
    if address != '':
        args = args & Q(address=address)
    if city != '':
        args = args & Q(city=city)
    if ident != '':
        args = args & Q(id=ident)
    if email != '':
        args = args & Q(email=email)
    if job_type != '':
        args = args & Q(job_type=job_type)
    if category != '':
        args = args & Q(category=category)

    print(args)

    try:
        #needs fixing
        search = calendar.objects.filter(args)
    except search.DoesNotExist:
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
    
    date_temp = request.POST['date']
    #converting string "date_temp" to datetime "date"
    if date_temp != "":
        cal.date = datetime.datetime.strptime(date_temp, '%Y/%m/%d')
    else:
        cal.date = None
    cal.surname = request.POST['surname']
    cal.name = request.POST['name']
    cal.address = request.POST['address']
    cal.city = request.POST['city']
    cal.phone = request.POST['phone']
    cal.email = request.POST['email']
    cal.job_type = request.POST['job_type']
    cal.category = request.POST['category']
    price_temp = request.POST['price']
    if price_temp != '':
        cal.price = price_temp
    else:
        cal.price = 0
    paid_temp = request.POST['paid']
    if paid_temp != '':
        cal.paid = paid_temp
    else:
        cal.price = 0
    cal.comments = request.POST['comments']
    # installationManual_temp = request.POST['file']
    # cal.installationManual = "Installation Manuals/" + installationManual_temp

    print(cal.installationManual)

    cal.save(force_insert=True)

    #after we finish the calendar insert we check if the client 
    #already exists or not and in the first case we need to 
    #create the new client

    cl = client()

    cl.surname = request.POST['surname']
    cl.name = request.POST['name']
    cl.address = request.POST['address']
    cl.city = request.POST['city']
    cl.phone = request.POST['phone']
    cl.email = request.POST['email']

    #Gathering all the given search parameters in order to search only for them
    args = Q()
    if cl.surname != '':
        args = args & Q(surname=cl.surname)
    if cl.name != '':
        args = args & Q(name=cl.name)
    if cl.address != '':
        args = args & Q(address=cl.address)
    if cl.city != '':
        args = args & Q(city=cl.city)
    if cl.phone != '':
        args = args & Q(phone=cl.phone)
    if cl.email != '':
        args = args & Q(email=cl.email)

    try:
        search = client.objects.filter(args)
        if search.exists():
            pass
        else:
            cl.save(force_insert=True)
    except search.DoesNotExist:
        return render(request, 'db.html')
    
    #This part (until the final render of the page) is needed for keeping the reports info on display
    dateStart = datetime.datetime.now() - datetime.timedelta(days=2*365)
    dateEnd = datetime.datetime.now() - datetime.timedelta(days=(1*365)-30)
    days = 335

    report_list = calendar.objects.raw("SELECT * FROM test_ent_calendar WHERE ( (job_type = 'ERROR' OR job_type = 'INSTALLATION' OR job_type = 'REMAKE') AND (category = 'ALARM' OR category = 'FIRE' OR category = 'CCTV') ) AND (date >= %s AND date <= %s)", [dateStart,dateEnd])
    # Show 1 calendar entry per page
    paginator = Paginator(report_list, 1) 

    #Getting the current page in order to move the next or previous
    page = request.GET.get('page')

    try:
        report = paginator.page(page)
        return render(request, 'db.html',{'report':report})
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        report = paginator.page(1)
        return render(request, 'db.html',{'report':report})
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        report = paginator.page(paginator.num_pages)
        return render(request, 'db.html',{'report':report})
    except calendar.DoesNotExist:
        return redirect ('db')


    return render(request, 'db.html',{'report':report})

def update_complete(request):

    # we search the tuple in database with the id provided
    # and then we update the rest of the values
    ident = request.POST['id']
    #We find the given calendar instance with the provided id and now we collent
    #the rest info in order to update
    cal = calendar.objects.get(id=ident)

    date_temp = request.POST['date']
    #converting string "date_temp" to datetime "date"
    if date_temp != "":
        cal.date = datetime.datetime.strptime(date_temp, '%Y/%m/%d')
    else:
        cal.date = cal.date
    surname_temp = request.POST['surname']
    if surname_temp != "":
        cal.surname = surname_temp
    else:
        cal.surname = cal.surname
    name_temp = request.POST['name']
    if name_temp != "":
        cal.name = name_temp
    else:
        cal.name = cal.name
    address_temp = request.POST['address']
    if address_temp != "":
        cal.address = address_temp
    else:
        cal.address = cal.address
    city_temp = request.POST['city']
    if city_temp != "":
        cal.city = city_temp
    else:
        cal.city = cal.city
    phone_temp = request.POST['phone']
    if phone_temp != "":
        cal.phone = phone_temp
    else:
        cal.phone = cal.phone
    email_temp = request.POST['email']
    if email_temp != "":
        cal.email = email_temp
    else:
        cal.email = cal.email
    job_type_temp = request.POST['job_type']
    if job_type_temp != "":
        cal.job_type = job_type_temp
    else:
        cal.job_type = cal.job_type
    category_temp = request.POST['category']
    if category_temp != "":
        cal.caregory = category_temp
    else:
        cal.category = cal.category
    price_temp = request.POST['price']
    if price_temp != '':
        cal.price = price_temp
    else:
        cal.price = cal.price
    paid_temp = request.POST['paid']
    if paid_temp != '':
        cal.paid = paid_temp
    else:
        cal.paid = cal.paid
    comments_temp = request.POST['comments']
    if comments_temp != "":
        cal.comments = comments_temp
    else:
        cal.comments = cal.comments
    installationManual_temp = request.POST['file']
    if installationManual_temp != "":
        cal.installationManual = "Installation Manuals/" + installationManual_temp
    else:
        cal.installationManual = cal.installationManual

    cal.save(update_fields=["date","surname","name","address","city","phone","email","job_type","category","price","paid","comments","installationManual"])
 
    #This part (until the final render of the page) is needed for keeping the reports info on display
    dateStart = datetime.datetime.now() - datetime.timedelta(days=2*365)
    dateEnd = datetime.datetime.now() - datetime.timedelta(days=(1*365)-30)
    days = 335

    report_list = calendar.objects.raw("SELECT * FROM test_ent_calendar WHERE ( (job_type = 'ERROR' OR job_type = 'INSTALLATION' OR job_type = 'REMAKE') AND (category = 'ALARM' OR category = 'FIRE' OR category = 'CCTV') ) AND (date >= %s AND date <= %s)", [dateStart,dateEnd])
    # Show 1 calendar entry per page
    paginator = Paginator(report_list, 1) 

    #Getting the current page in order to move the next or previous
    page = request.GET.get('page')

    try:
        report = paginator.page(page)
        return render(request, 'db.html',{'report':report})
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        report = paginator.page(1)
        return render(request, 'db.html',{'report':report})
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        report = paginator.page(paginator.num_pages)
        return render(request, 'db.html',{'report':report})
    except calendar.DoesNotExist:
        return redirect ('db')


    return render(request, 'db.html',{'report':report})


def search_complete_client(request):

    search = client()

    ident = request.POST['id']
    surname = request.POST['surname']
    name = request.POST['name']
    address = request.POST['address']
    city = request.POST['city']
    phone = request.POST['phone']
    email = request.POST['email']

    #Gathering all the given search parameters in order to search only for them
    args = Q()
    if surname != '':
        args = args & Q(surname=surname)
    if phone != '':
        args = args & Q(phone=phone)
    if name != '':
        args = args & Q(name=name)
    if address != '':
        args = args & Q(address=address)
    if city != '':
        args = args & Q(city=city)
    if ident != '':
        args = args & Q(id=ident)
    if email != '':
        args = args & Q(email=email)

    try:
        search = client.objects.filter(args)
    except search.DoesNotExist:
        return render(request, 'db.html')
    # except client.AttributeError:
    #     return render(request, 'db.html')

    # print(search.date,search.surname,search.name,search.address,search.city,
    #     search.phone,search.email,search.job_type,search.category)

    return render(request, 'search_complete_client.html', {'search':search})
    # return render(request, 'search_complete.html')

def insert_complete_client(request):

    #getting the input from insert page
    #and we are entering it to the database

    #first we create the client item to hold the client input
    cl = client()
    
    cl.surname = request.POST['surname']
    cl.name = request.POST['name']
    cl.address = request.POST['address']
    cl.city = request.POST['city']
    cl.phone = request.POST['phone']
    cl.email = request.POST['email']

    #Gathering all the given search parameters in order to search only for them
    args = Q()
    if cl.surname != '':
        args = args & Q(surname=cl.surname)
    if cl.name != '':
        args = args & Q(name=cl.name)
    if cl.address != '':
        args = args & Q(address=cl.address)
    if cl.city != '':
        args = args & Q(city=cl.city)
    if cl.phone != '':
        args = args & Q(phone=cl.phone)
    if cl.email != '':
        args = args & Q(email=cl.email)

    try:
        search = client.objects.filter(args)
        if search.exists():
            pass
        else:
            cl.save(force_insert=True)
    except search.DoesNotExist:
        return render(request, 'db.html', {'name':'Theo'})

    #This part (until the final render of the page) is needed for keeping the reports info on display
    dateStart = datetime.datetime.now() - datetime.timedelta(days=2*365)
    dateEnd = datetime.datetime.now() - datetime.timedelta(days=(1*365)-30)
    days = 335

    report_list = calendar.objects.raw("SELECT * FROM test_ent_calendar WHERE ( (job_type = 'ERROR' OR job_type = 'INSTALLATION' OR job_type = 'REMAKE') AND (category = 'ALARM' OR category = 'FIRE' OR category = 'CCTV') ) AND (date >= %s AND date <= %s)", [dateStart,dateEnd])
    # Show 1 calendar entry per page
    paginator = Paginator(report_list, 1) 

    #Getting the current page in order to move the next or previous
    page = request.GET.get('page')

    try:
        report = paginator.page(page)
        return render(request, 'db.html',{'report':report})
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        report = paginator.page(1)
        return render(request, 'db.html',{'report':report})
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        report = paginator.page(paginator.num_pages)
        return render(request, 'db.html',{'report':report})
    except calendar.DoesNotExist:
        return redirect ('db')


    return render(request, 'db.html',{'report':report})

def update_complete_client(request):

    # we search the tuple in database with the id provided
    # and then we update the rest of the values
    ident = request.POST['id']

    cl = client.objects.get(id=ident)

    surname_temp = request.POST['surname']
    if surname_temp != "":
        cl.surname = surname_temp
    else:
        cl.surname = cl.surname
    name_temp = request.POST['name']
    if name_temp != "":
        cl.name = name_temp
    else:
        cl.name = cl.name
    address_temp = request.POST['address']
    if address_temp != "":
        cl.address = address_temp
    else:
        cl.address = cl.address
    city_temp = request.POST['city']
    if city_temp != "":
        cl.city = city_temp
    else:
        cl.city = cl.city
    phone_temp = request.POST['phone']
    if phone_temp != "":
        cl.phone = phone_temp
    else:
        cl.phone = cl.phone
    email_temp = request.POST['email']
    if email_temp != "":
        cl.email = email_temp
    else:
        cl.email = cl.email
    comments_temp = request.POST['comments']
    if comments_temp != "":
        cl.comments = comments_temp
    else:
        cl.comments = cl.comments

    cl.save(update_fields=["surname","name","address","city","phone","email","comments"])

    #This part (until the final render of the page) is needed for keeping the reports info on display
    dateStart = datetime.datetime.now() - datetime.timedelta(days=2*365)
    dateEnd = datetime.datetime.now() - datetime.timedelta(days=(1*365)-30)
    days = 335

    report_list = calendar.objects.raw("SELECT * FROM test_ent_calendar WHERE ( (job_type = 'ERROR' OR job_type = 'INSTALLATION' OR job_type = 'REMAKE') AND (category = 'ALARM' OR category = 'FIRE' OR category = 'CCTV') ) AND (date >= %s AND date <= %s)", [dateStart,dateEnd])
    # Show 1 calendar entry per page
    paginator = Paginator(report_list, 1) 

    #Getting the current page in order to move the next or previous
    page = request.GET.get('page')

    try:
        report = paginator.page(page)
        return render(request, 'db.html',{'report':report})
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        report = paginator.page(1)
        return render(request, 'db.html',{'report':report})
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        report = paginator.page(paginator.num_pages)
        return render(request, 'db.html',{'report':report})
    except calendar.DoesNotExist:
        return redirect ('db')


    return render(request, 'db.html',{'report':report})


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