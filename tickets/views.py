import sys
import datetime
from django.views.generic import ListView, DetailView
from django.template import RequestContext
from tickets.forms import LogInForm, DocumentForm
from django.shortcuts import render_to_response, render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.utils.decorators import method_decorator
from .models import TicketAge ,Category, Ticket, Comment, User, Employee, Document
#from .forms import TicketForm
SYSTEM_NAME='PTS'
def ticketing_login(request):
   
     if request.session.get('is_logged_in', False):
        co = Category.objects.all()
        query = "Select *, weekdays(created::date,now()::date) AS age FROM tickets_ticket ORDER BY created DESC"
        tick = Ticket.objects.raw(query)
        count = Ticket.objects.filter(flag=True,assign_user_id=request.user.id).count()
        user = User.objects.get(id=request.user.id)
        return render(request, './ticket/home.html', {'Ticket': tick,'Category': co, 
                      'system_name': SYSTEM_NAME, 'user': user,'count':count, 
                      'datetime': datetime.datetime.now()})

     if request.method == 'POST':
        userid = request.POST.get('userID')
        passwords = request.POST.get('password')
        user = auth.authenticate(username=userid, password=passwords)
        if user is not None and user.is_active:
           auth.login(request,user)
           co = Category.objects.all()
           query = "Select *, weekdays(created::date,now()::date) AS age FROM tickets_ticket ORDER BY created DESC"
           tick = Ticket.objects.raw(query)
           request.session['is_logged_in'] = True
           count = Ticket.objects.filter(flag=True, assign_user_id=request.user.id).count()
           
           return render(request, './ticket/home.html', {'Ticket': tick,'Category': co, 
                        'system_name': SYSTEM_NAME, 'user': user, 'count':count,
                        'datetime': datetime.datetime.now()})
        
        else:
        
           return HttpResponseRedirect('/')
     
     else:
         form=LogInForm()
         return render(request,'login.html',{'form': form,'system_name': SYSTEM_NAME,
                     'cover_url':'static/images/19th_logo.jpg'})

@login_required(login_url='/')
def open_ticket(request):
   openticket = True
   status = False
   co = Category.objects.all()
   users = User.objects.all()
   user = User.objects.get(id=request.user.id)
   count = Ticket.objects.filter(flag=True, assign_user_id=request.user.id).count()
   
   return render(request,'./ticket/tickets.html', {'system_name': SYSTEM_NAME,
                'user': user,'Category': co, 'Users':users, 'count':count, 'open': openticket, 'status': status})

@login_required(login_url='/')
def search_ticket(request):
   category_filter = request.GET.get('ticket_search_filters')
   search = request.GET.get('seach_ticket')
   co = Category.objects.all()
   ticket = Ticket.objects.filter(category=category_filter,subject__istartswith=search)
   count = Ticket.objects.filter(flag=True,assign_user_id=request.user.id ).count()
   user = User.objects.get(id=request.user.id)
   return render(request, './ticket/home.html', {'Ticket': ticket,'Category': co,
                'system_name': SYSTEM_NAME, 'user': user,'count':count})

@login_required(login_url='/')
def view_profile(request, pk):
   employee = Employee.objects.get(user_id=pk)
   count = Ticket.objects.filter(flag=True,assign_user_id=request.user.id ).count()
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
       if assign_user == 'blank' or Ticket.objects.filter(user_requestor_id=requestor,category_id=category,assign_user_id=assign_user).exists() and Ticket.objects.filter(subject=subjects):
         return HttpResponseRedirect('/openticket/')
       else:
           
         ticket = Ticket(subject= subjects, description=description, user_requestor_id=requestor,status=1,flag=1,priority=2,category_id=category,created_by_id=created_user,assign_user_id=assign_user)
         ticket.save()
         ticket=Ticket.objects.latest('id')
         ticket_age= TicketAge(assign_user_id=assign_user, ticket_id=ticket.id, done=True)
         ticket_age.save()
              #ticket = Ticket.objects.get(created_by_id=created_user,subject=subjects,category_id=category)
         c = Comment(comment='Subject: '+ subjects +' \n\n Description:\n '+description+'\n\n Assign User: '+ ticket.assign_user.get_full_name()+'\n\n Category: '+ticket.category.name+'\n\n Requester: '+ticket.user_requestor.get_full_name(), user_id = created_user, ticket_id=ticket.id)
         c.save()  
         return HttpResponseRedirect('/')
    else:
       if Ticket.objects.filter(id=ticket_edit).exists():
        ticket = Ticket.objects.get(id=ticket_edit)
        if ticket.subject != subjects:
          c = Comment(comment='Edited Subject "'+ subjects + '" ', user_id = created_user, ticket_id=ticket.id)
          Ticket.objects.filter(id=ticket_edit).update(subject=subjects, flag=True)
          c.save()
        if ticket.description != description:
          c = Comment(comment='Edited Description "'+ description+ '" ', user_id = created_user, ticket_id=ticket.id)
          Ticket.objects.filter(id=ticket_edit).update(description=description, flag=True)
          c.save()
        if ticket.user_requestor_id != int(requestor):
          user = User.objects.get(id=requestor)
          c = Comment(comment='Requestor "'+ user.get_full_name() + '" ', user_id = created_user, ticket_id=ticket.id)
          Ticket.objects.filter(id=ticket_edit).update(user_requestor=requestor, flag=True)
          c.save()
        if ticket.category_id != int(category):
          cat = Category.objects.get(id=category)
          c = Comment(comment='Edited Category "'+ cat.name + '" ', user_id = created_user, ticket_id=ticket.id)
          Ticket.objects.filter(id=ticket_edit).update(category=category, flag=True)
          c.save()  
        if ticket.assign_user_id != int(assign_user):
          user = User.objects.get(id=assign_user)
          TicketAge.objects.filter(ticket_id=ticket_edit).update(modified=datetime.datetime.now(), done=False)
          t=TicketAge(assign_user_id=assign_user,ticket_id=ticket_edit, done=True)
          t.save()
          c = Comment(comment='Assigned User "'+ user.get_full_name() + '" ', user_id = created_user, ticket_id=ticket.id)
          Ticket.objects.filter(id=ticket_edit).update(assign_user=assign_user, flag=True)
          c.save()

        return HttpResponseRedirect('/ticketdetailed/'+ticket_edit+'/')
     
@login_required(login_url='/')
def view_ticket(request, pk):
    open_button=True
    form = DocumentForm()
    t = Ticket.objects.get(id=pk)
    if t.status:  
      query="Select *, justify_hours(age(now(),created) ) AS hours FROM tickets_ticketage Where ticket_id="+pk+" and done=True and assign_user_id="+str(t.assign_user_id)
    else:
      query="Select *, justify_hours(age(modified,created) ) AS hours FROM tickets_ticketage Where ticket_id="+pk+" and assign_user_id="+str(t.assign_user_id)
    ticket_age=TicketAge.objects.raw(query)
    for x in ticket_age:
      time=microseconds(str(x.hours))
    if request.user.id == t.assign_user_id:  
      Ticket.objects.filter(id=pk).update(flag=False)
    c = Comment.objects.filter(ticket_id=pk).order_by('-created')
    document = Document.objects.filter(ticket_id=pk)
    count = Ticket.objects.filter(flag=True, assign_user_id=request.user.id).count()
    user = User.objects.get(id=request.user.id)
    return render(request,'./ticket/tickets.html', {'system_name': SYSTEM_NAME,'ticket': t,'user': user, 
              'Comment':c, 'count':count, 'form': form, 'documents': document, 'com_button':open_button,'ticket_age':time, 'datetime':datetime.datetime.now()})

@login_required(login_url='/')
def edit_ticket(request, pk):
  edit_open=True
  co = Category.objects.all()
  users = User.objects.all()
  form = DocumentForm()
  t = Ticket.objects.get(id=pk)
  if request.user.id == t.assign_user_id:  
     Ticket.objects.filter(id=pk).update(flag=False)
  c = Comment.objects.filter(ticket_id=pk).order_by('-created')
  document = Document.objects.filter(ticket_id=pk)
  count = Ticket.objects.filter(flag=True, assign_user_id=request.user.id).count()
  user = User.objects.get(id=request.user.id)
  return render(request,'./ticket/tickets.html', {'system_name': SYSTEM_NAME,
              'ticket': t,'user': user, 'Category': co, 'Users':users,'Comment':c,'edit': edit_open ,'count':count,'open':edit_open,'form': form, 'documents': document})

@login_required(login_url='/')
def close_status_ticket(request,pk):
   c = Comment(comment='Ticket Closed.', user_id = request.user.id, ticket_id=pk)
   ticket=Ticket.objects.get(id=pk)
   Ticket.objects.filter(id=pk).update(status=False, flag=True, modified=datetime.datetime.now())
   TicketAge.objects.filter(ticket_id=pk, assign_user_id=ticket.assign_user, done=True).update(done=False, modified=datetime.datetime.now())
   c.save()
   return HttpResponseRedirect('/ticketdetailed/'+pk+'/')

def open_status_ticket(request,pk):
   c = Comment(comment='Ticket Reopend.', user_id = request.user.id, ticket_id=pk)
   t=Ticket.objects.get(id=pk)
   Ticket.objects.filter(id=pk).update(status=True, flag=True)
   t = TicketAge(ticket_id=pk, done=True, assign_user_id=t.assign_user_id)
   t.save()
   c.save()
   return HttpResponseRedirect('/ticketdetailed/'+pk+'/')

@login_required(login_url='/')
def view_notification(request):
    t = Ticket.objects.filter(assign_user_id=request.user.id)
    count = Ticket.objects.filter(flag=True, assign_user_id=request.user.id).count()
    user = User.objects.get(id=request.user.id)
    return render(request,'./ticket/notification.html', {'system_name': SYSTEM_NAME,
                  'ticket': t,'user': user, 'count':count, 'datetime':datetime.datetime.now()})

@login_required(login_url='/')
def view_request(request):
    t = Ticket.objects.filter(user_requestor_id=request.user.id)
    count = Ticket.objects.filter(flag=True, assign_user_id=request.user.id).count()
    user = User.objects.get(id=request.user.id)
    return render(request,'./ticket/notification.html', {'system_name': SYSTEM_NAME,
                  'ticket': t,'user': user, 'count':count, 'datetime':datetime.datetime.now()})

@login_required(login_url='/')
def set_comment(request):
    context = RequestContext(request)
    com = request.GET.get('_comment')
    ticket_id = request.GET.get('_ticket')
    c=Comment.objects.create(comment=com,user_id=request.user.id, ticket_id = ticket_id)
    c.save()
    co=Comment.objects.filter(ticket_id=ticket_id).order_by('-created')
    #ss='<div> <h1>'+com+'</h1></div>'
    #return HttpResponse(s)  
    return render_to_response('ticket/comment_detail.html', {'Comment': co,
                              'datetime':datetime.datetime.now()}, context)

@login_required(login_url='/')
def tickets_assign(request,pk):
    t = Ticket.objects.filter(assign_user_id=pk)
    count = Ticket.objects.filter(flag=True, assign_user_id=request.user.id).count()
    user = User.objects.get(id=request.user.id)
    return render(request,'./ticket/notification.html', {'system_name': SYSTEM_NAME,
                'ticket': t,'user': user, 'count':count})

@login_required(login_url='/')
def tickets_request(request,pk):
    t = Ticket.objects.filter(user_requestor_id=pk)
    count = Ticket.objects.filter(flag=True, assign_user_id=request.user.id).count()
    user = User.objects.get(id=request.user.id)
    return render(request,'./ticket/notification.html', {'system_name': SYSTEM_NAME,
                  'ticket': t,'user': user, 'count':count})

def upload(request,pk):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        lis = request.FILES['docfile'].name
        if form.is_valid():
            newdoc = Document(docfile = request.FILES['docfile'],name=lis,ticket_id=pk, user_id=request.user.id)
            c=Comment.objects.create(comment='Uploaded file '+lis,user_id=request.user.id, ticket_id = pk)
            newdoc.save()
            c.save()
            
    return HttpResponseRedirect('/ticketdetailed/'+pk+'/')

def about(request):
  
    count = Ticket.objects.filter(flag=True,assign_user_id=request.user.id).count()
    user = User.objects.get(id=request.user.id)
    return render(request, './about_us.html', {'system_name': SYSTEM_NAME, 'user': user,'count':count})

def microseconds(time):
    return time[0:time.find('.')]

# def month(time):
#   return time.month

