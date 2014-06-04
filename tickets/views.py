import sys
import datetime

from django.views.generic import ListView, DetailView
from django.template import RequestContext
from django.shortcuts import render_to_response, render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator, InvalidPage, EmptyPage

from .models import TicketAge
from .models import Category
from .models import Ticket
from .models import Comment
from .models import User
from .models import Employee
from .models import Attachment

from tickets.forms import LogInForm, DocumentForm

SYSTEM_NAME='PTS'


def ticketing_login(request, *args):
     if request.session.get('is_logged_in', False):
         employee = Employee.objects.get(user_id=request.user.id)
         return home(request, 'open_status','','',False,'home', employee)

     if request.method == 'POST':
        userid = request.POST.get('userID')
        passwords = request.POST.get('password')
        user = auth.authenticate(username=userid, password=passwords)
        if user is not None and user.is_active:
           auth.login(request,user)
           if Employee.objects.filter(user_id=request.user.id).exists():
                employee = Employee.objects.get(user_id=request.user.id)
                request.session['is_logged_in'] = True
                return home(request, 'open_status','','',False, 'home', employee)
           else:
                return HttpResponseRedirect('/')
        else:

           return HttpResponseRedirect('/')

     else:
         form=LogInForm()
         return render(request,'login.html',{'form': form,'system_name': 'Phlhealth ARMM Ticketing System',
                     'cover_url':'static/images/19th_logo.jpg'})

@login_required(login_url='/')
def all_tickets(request):
    employee = Employee.objects.get(user_id=request.user.id)
    return home(request, 'all_tickets','','',False,'all_ticket',employee)

@login_required(login_url='/')
def closed_tickets(request):
    employee = Employee.objects.get(user_id=request.user.id)
    return home(request, 'closed_tickets','','',False,'closed',employee)

@login_required(login_url='/')
def home(request, *args):
    data = {'system_name' : SYSTEM_NAME}
    limit = 15
    total_rows = 0
    co = Category.objects.all()  
    if args[0] == 'open_status':
        ticket = Ticket.objects.extra(select = {'age':'weekdays(created::date,now()::date)'}, order_by=['-created']).filter(status=True,assigned_id=request.user.id)
        total_rows = ticket.count()
    else:
        ticket = Ticket.objects.extra(select = {'age':'weekdays(created::date,now()::date)'}, order_by=['-created'])
        total_rows = ticket.count()
    count = Ticket.objects.filter(flag=True,assigned=request.user.id).count()
    user = User.objects.get(id=request.user.id)
    
        
    data['current_offset'] = request.GET.get('offset', 0)
    data['offset_list'] = get_offsets(total_rows, limit)        
    data['Ticket'] = ticket[data['current_offset']: int(data['current_offset']) + limit]
    data['Category'] = co
    data['user'] = user
    data['count'] = count
    data['datetime'] = datetime.datetime.now()
    data['state'] = args[0]
    data[args[4]] = 'active'
    data['employee'] = args[5]
    data['quick_search'] = True

    return render(request, './ticket/home.html',data)


@login_required(login_url='/')
def open_ticket(request):
    data = {'system_name' : SYSTEM_NAME}
    openticket = True
    status = False
    co = Category.objects.all()
    employee = Employee.objects.get(user_id=request.user.id)
    users = User.objects.all()
    user = User.objects.get(id=request.user.id)
    count = Ticket.objects.filter(flag=True, assigned=request.user.id).count()
    data['user'] = user
    data['Category'] = co
    data['open_ticket'] = 'active'
    data['Users'] = users
    data['count'] = count
    data['open'] = openticket
    data['status'] = status
    data['employee'] = employee

    return render(request,'./ticket/tickets.html', data)


@login_required(login_url='/')
def search_ticket(request):
    data = {'system_name' : SYSTEM_NAME}
    category_filter = request.GET.get('ticket_search_filters')
    search = request.GET.get('seach_ticket')
    state = request.GET.get('state')
    co = Category.objects.all()
    ticket = Ticket.objects.filter(category=category_filter, subject__istartswith=search).extra(select = {'age':'weekdays(created::date,now()::date)'})
    count = Ticket.objects.filter(flag=True, assigned_id=request.user.id ).count()
    user = User.objects.get(id=request.user.id)
    data['user'] = user
    data['Category'] = co
    data['state'] = state
    data['Ticket'] = ticket
    data['count'] = count
   

    return render(request, './ticket/home.html', data)


@login_required(login_url='/')
def advance_search_ticket(request):
    category = request.GET.get('category_advance')
    subject = request.GET.get('subject_advance')
    ticket_status = request.GET.get('status_advance')
    description = request.GET.get('description_advance')
    assign_user = request.GET.get('assign_user_advance')
    requestor = request.GET.get('request_user_advance')
    employee = Employee.objects.get(user_id=request.user.id)
    count = Ticket.objects.filter(flag=True,assigned_id=request.user.id ).count()
    user = User.objects.get(id=request.user.id)
    query=''
    first = True

    if subject == '' and description == '' and ticket_status == '' and assign_user == '' and category == '' and requestor == '':
        return HttpResponseRedirect('/advance_search')
    else:
        data = {'system_name' : SYSTEM_NAME}   
        try:
            if subject != '':
                query = " subject like '%%"+ subject+"%%'"
                first = False
            if description != '':
                if first:
                    query += " description like '%%"+ description+"%%'"
                    first = False
                else:
                    query += " and description like '%%"+ description+"%%'"
            if ticket_status:
                if first:
                    query += " status = True"
                    first = False
                else:
                    query += " and status = True"
            if ticket_status == 'close':
                if first:
                    query += " status = False"
                    first = False
                else:
                    query += " and status = False"
            if assign_user != '':
                if first:
                    query += " assigned_id = "+ assign_user
                    first = False
                else:
                    query += " and assigned_id = "+ assign_user
            if category != '':
                if first:
                    query += " category_id = "+category
                    first = False
                else:
                    query += " and category_id = "+category
            if requestor != '':
                if first:
                    query += " requester_id = "+requestor
                    first = False
                else:
                    query += " and requester_id = "+requestor

            ticket = Ticket.objects.raw("Select *, weekdays(created::date,now()::date) as age From ticket where "+query)
            
            queries_without_page = request.GET.copy()

            if queries_without_page.has_key('page'):
                del queries_without_page['page']

            paginator = Paginator(ticket, 5)
            try: page = int(request.GET.get("page", '1'))
            except ValueError: page = 1

            try:
                ticket = paginator.page(page)
            except (InvalidPage, EmptyPage):
                ticket = paginator.page(paginator.num_pages)
        except:
              print sys.exc_info()[0], sys.exc_info()[1]    

        data['Ticket'] = ticket
        data['count'] = count
        data['state'] = 'all_tickets'
        data['employee'] = employee
        data['query_params'] = queries_without_page
        
        return render(request, './ticket/advance_search_result.html', data)

@login_required(login_url='/')
def view_profile(request, pk):
   employee = Employee.objects.get(user_id=pk)
   count = Ticket.objects.filter(flag=True,assigned_id=request.user.id ).count()
   user = User.objects.get(id=request.user.id)
   print employee.image_path
   return render(request, './employee_profile.html', {'system_name': SYSTEM_NAME, 'user': user,'employee':employee, 'count':count})


@login_required(login_url='/')
def save_ticket(request):
    ticket_edit = request.POST.get('ticket_edit')
    subjects = request.POST.get('ticket_subject')
    description = request.POST.get('description')
    assign_user = request.POST.get('user_choose')
    category = request.POST.get('category_choose')
    requestor = request.POST.get('requestor_choose')
    created_user = request.user.id
    stat = request.POST.get('status_choose')
    if ticket_edit == '':
       if assign_user == 'blank' or Ticket.objects.filter(requester_id=requestor,category_id=category,assigned=assign_user).exists() and Ticket.objects.filter(subject=subjects):
         return HttpResponseRedirect('/openticket/')
       else:

         ticket = Ticket(subject=subjects, description=description, requester_id=requestor, status=1,flag=1, priority=2, category_id=category, created_by_id=created_user, assigned_id=assign_user)
         ticket.save()
         ticket=Ticket.objects.latest('id')
         ticket_age= TicketAge(assigned_id=assign_user, ticket_id=ticket.id, done=True)
         ticket_age.save()
         c = Comment(comment='Subject: '+ subjects +' \n\n Description:\n '+description+'\n\n Assigned User: '+ ticket.assigned.get_full_name()+'\n\n Category: '+ticket.category.name+'\n\n Requester: '+ticket.requester.get_full_name(), user_id = created_user, ticket_id=ticket.id)
         c.save()
         return HttpResponseRedirect('/')
    else:
        if Ticket.objects.filter(id=ticket_edit).exists():
            ticket = Ticket.objects.get(id=ticket_edit)
            comments=''
            if ticket.subject != subjects:
                comments = 'Edited Subject: "'+ subjects + '" \n\n '
                Ticket.objects.filter(id=ticket_edit).update(subject=subjects, flag=True)

            if ticket.description != description:
                comments += 'Edited Description: "'+ description+ '" \n\n '
                Ticket.objects.filter(id=ticket_edit).update(description=description, flag=True)

            if ticket.requester_id != int(requestor):
                user = User.objects.get(id=requestor)
                comments += 'Requester: "'+ user.get_full_name() + '" \n\n '
                Ticket.objects.filter(id=ticket_edit).update(requester=requestor, flag=True)

            if ticket.category_id != int(category):
                cat = Category.objects.get(id=category)
                comments += 'Edited Category: "'+ cat.name + '" \n\n '
                Ticket.objects.filter(id=ticket_edit).update(category=category, flag=True)

            if ticket.assigned_id != int(assign_user):
                user = User.objects.get(id=assign_user)
                TicketAge.objects.filter(ticket_id=ticket_edit).update(modified=datetime.datetime.now(), done=False)
                t=TicketAge(assigned_id=assign_user,ticket_id=ticket_edit, done=True)
                t.save()
                comments += 'Assigned User: "'+ user.get_full_name() + '" '
                Ticket.objects.filter(id=ticket_edit).update(assigned=assign_user, flag=True)

            c = Comment(comment= comments, user_id = created_user, ticket_id=ticket.id)
            c.save()
        return HttpResponseRedirect('/ticketdetailed/'+ticket_edit+'/')


@login_required(login_url='/')
def view_ticket(request, pk):
    data = {'system_name' : SYSTEM_NAME}   
    open_button=True
    form = DocumentForm()
    t = Ticket.objects.get(id=pk)
    print pk
    print pk
    if t.status:
      query="Select *, justify_hours(age(now(),created) ) AS hours FROM ticketage where ticket_id="+ pk +" and done=True and assigned_id=" + str(t.assigned_id)
    else:
      query="Select *, justify_hours(age(modified,created) ) AS hours FROM ticketage where ticket_id="+ pk +" and assigned_id=" + str(t.assigned_id)
    print "t.assigned", t.assigned_id
    ticket_age=TicketAge.objects.raw(query)
    for x in ticket_age:
        time=microseconds(str(x.hours))
    if request.user.id == t.assigned_id:
      Ticket.objects.filter(id=pk).update(flag=False)
    c = Comment.objects.filter(ticket_id=pk).order_by('-created')
    attachment = Attachment.objects.filter(ticket_id=pk)
    count = Ticket.objects.filter(flag=True, assigned=request.user.id).count()
    user = User.objects.get(id=request.user.id)
    employee = Employee.objects.get(user_id=request.user.id)

    data['ticket'] = t
    data['user'] = user
    data['Comment'] = c
    data['count'] = count
    data['form'] = form
    data['employee'] = employee
    data['attachments'] = attachment
    data['com_button'] = open_button
    data['ticket_age'] = time
    data['datetime'] = datetime.datetime.now()

    return render(request,'./ticket/tickets.html', data)


@login_required(login_url='/')
def edit_ticket(request, pk):
  data = {'system_name' : SYSTEM_NAME}   
  edit_open=True
  co = Category.objects.all()
  users = User.objects.all()
  form = DocumentForm()
  t = Ticket.objects.get(id=pk)
  if request.user.id == t.assigned_id:
     Ticket.objects.filter(id=pk).update(flag=False)
  c = Comment.objects.filter(ticket_id=pk).order_by('-created')
  attachment = Attachment.objects.filter(ticket_id=pk)
  count = Ticket.objects.filter(flag=True, assigned_id=request.user.id).count()
  user = User.objects.get(id=request.user.id)
 
  data['ticket'] = t
  data['user'] = user
  data['Category'] = co
  data['Users'] = users
  data['Comment'] = c
  data['edit'] = edit_open
  data['count'] = count
  data['open'] = edit_open
  data['form'] = form
  data['attachments'] = attachment

  return render(request,'./ticket/tickets.html', data)


@login_required(login_url='/')
def close_status_ticket(request,pk):
   c = Comment(comment='Ticket Closed.', user_id=request.user.id, ticket_id=pk)
   ticket=Ticket.objects.get(id=pk)
   Ticket.objects.filter(id=pk).update(status=False, flag=True, modified=datetime.datetime.now())
   TicketAge.objects.filter(ticket_id=pk, assigned_id=ticket.assigned, done=True).update(done=False, modified=datetime.datetime.now())
   c.save()
   return HttpResponseRedirect('/ticketdetailed/'+pk+'/')


def open_status_ticket(request,pk):
    c = Comment(comment='Ticket Re-opened.', user_id = request.user.id, ticket_id=pk)
    t=Ticket.objects.get(id=pk)
    Ticket.objects.filter(id=pk).update(status=True, flag=True)
    t = TicketAge(ticket_id=pk, done=True, assigned_id=t.assigned_id)
    t.save()
    c.save()
    return HttpResponseRedirect('/ticketdetailed/'+pk+'/')


@login_required(login_url='/')
def view_notification(request):
    data = {'system_name' : SYSTEM_NAME}
    t = Ticket.objects.filter(assigned=request.user.id)
    count = Ticket.objects.filter(flag=True, assigned=request.user.id).count()
    user = User.objects.get(id=request.user.id)
    employee = Employee.objects.get(user_id=request.user.id)
    
    data['ticket'] = t
    data['user'] = user
    data['employee'] = employee
    data['count'] = count
    data['notification'] = 'active'
    data['datetime'] = datetime.datetime.now()
    data['quick_search'] = True
    
    return render(request,'./ticket/notification.html', data)


@login_required(login_url='/')
def view_request(request):
    data = {'system_name' : SYSTEM_NAME}
    t = Ticket.objects.filter(requester=request.user.id)
    count = Ticket.objects.filter(flag=True, assigned=request.user.id).count()
    user = User.objects.get(id=request.user.id)
    employee = Employee.objects.get(user_id=request.user.id)

    data['ticket'] = t
    data['user'] = user
    data['employee'] = employee
    data['count'] = count
    data['notification'] = 'active'
    data['datetime'] = datetime.datetime.now()
    data['quick_search'] = True
    
    return render(request,'./ticket/notification.html', data)

@login_required(login_url='/')
def set_comment(request):
    context = RequestContext(request)
    com = request.GET.get('_comment')
    ticket_id = request.GET.get('_ticket')
    Ticket.objects.filter(id=ticket_id).update(flag=True)
    c=Comment.objects.create(comment=com,user_id=request.user.id, ticket_id = ticket_id)
    c.save()
    co=Comment.objects.filter(ticket_id=ticket_id).order_by('-created')

    return render_to_response('ticket/comment_detail.html', {'Comment': co,
                              'datetime':datetime.datetime.now()}, context)


@login_required(login_url='/')
def tickets_assign(request,pk):
    t = Ticket.objects.filter(assigned_id=pk)
    count = Ticket.objects.filter(flag=True, assigned_id=request.user.id).count()
    user = User.objects.get(id=request.user.id)
    return render(request,'./ticket/notification.html', {'system_name': SYSTEM_NAME,
                'ticket': t,'user': user, 'count':count})


@login_required(login_url='/')
def tickets_request(request,pk):
    t = Ticket.objects.filter(requester_id=pk)
    count = Ticket.objects.filter(flag=True, assigned_id=request.user.id).count()
    user = User.objects.get(id=request.user.id)
    return render(request,'./ticket/notification.html', {'system_name': SYSTEM_NAME,
                  'ticket': t,'user': user, 'count':count})


@login_required(login_url='/')
def upload(request,pk):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        lis = request.FILES['docfile'].name
        if form.is_valid():
            newdoc = Attachment(docfile = request.FILES['docfile'],name=lis,ticket_id=pk, user_id=request.user.id)
            c=Comment.objects.create(comment='Uploaded file '+lis,user_id=request.user.id, ticket_id = pk)
            newdoc.save()
            c.save()

    return HttpResponseRedirect('/ticketdetailed/'+pk+'/')


@login_required(login_url='/')
def about(request):
    employee = Employee.objects.get(user_id=request.user.id)
    count = Ticket.objects.filter(flag=True,assigned_id=request.user.id).count()
    user = User.objects.get(id=request.user.id)
    return render(request, './about_us.html', {'system_name': SYSTEM_NAME, 'user': user,'count':count, 'employee':employee})


@login_required(login_url='/')
def advance_search(request):
    data = {'system_name' : SYSTEM_NAME}
    category = Category.objects.all()
    ticket = Ticket.objects.all()
    count = Ticket.objects.filter(flag=True,assigned_id=request.user.id ).count()
    user = User.objects.all()
    employee = Employee.objects.get(user_id=request.user.id)
    
    data['Ticket'] = ticket
    data['Category'] = category
    data['employee'] = employee
    data['users'] = user
    data['count'] = count

    return render(request, './ticket/advance_search.html', data)


def microseconds(time):
    return time[0:time.find('.')]

def prev_offset(of, lm):
    if of-lm<0:
        return of
    else:
        return of-lm

def next_offset(of, lm, size):
    if of+lm>size:
        return of
    else:
        return of+lm


def get_offsets(total_rows, limit):
    offset_list = []
    pages = 0
    if total_rows%limit>0:
        pages = (total_rows//limit) + 1
    else:
        pages = (total_rows//limit)
    offset = 0
    for i in range(pages):
        offset_list.append({'page_num': (i+1),
                            'offset'  : offset})
        offset = offset + limit
    return offset_list
