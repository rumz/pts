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
import sys, datetime
from .models import TicketAge ,Category, Ticket, Comment, User, Employee, Document
#from .forms import TicketForm

def ticketing_login(request):
  userid = request.POST.get('userID')
  passwords = request.POST.get('password')
  if request.session.get('is_logged_in', False):
    co = Category.objects.all()
    query = "Select *, date_part('days', now()-created) AS days FROM tickets_ticket"
    tick = Ticket.objects.raw(query)
    count = Ticket.objects.filter(flag=True,assign_user_id=request.session['userID'] ).count()
    user = User.objects.get(id=request.session['userID'])
    return render(request, './ticket/home.html', {'Ticket': tick,'Category': co, 'system_name': 'Document Tracker System', 'user': user,'count':count})

  if request.method == 'POST':
    user = auth.authenticate(username=userid, password=passwords)
    if user is not None and user.is_active:
      auth.login(request,user)
      co = Category.objects.all()
      query = "Select *, date_part('days', now()-created) AS days FROM tickets_ticket"
      tick = Ticket.objects.raw(query)
      request.session['is_logged_in'] = True
      request.session['userID'] = user.id
      request.session['name'] = user.get_full_name()
      count = Ticket.objects.filter(flag=True, assign_user_id=request.session['userID']).count()
     
      return render(request, './ticket/home.html', {'Ticket': tick,'Category': co, 'system_name': 'Document Tracker System', 'user': user, 'count':count})
    
    else:
    
      return HttpResponseRedirect('/')
  
  else:
      form=LogInForm()
      return render(request,'login.html',{'form': form,'system_name': 'Document Tracker System',
                                                'cover_url':'static/images/19th_logo.jpg'})
@login_required(login_url='/')
def open_ticket(request):
  openticket = True
  co = Category.objects.all()
  users = User.objects.all()
  user = User.objects.get(id=request.session['userID'])
  count = Ticket.objects.filter(flag=True, assign_user_id=request.session['userID']).count()
  
  return render(request,'./ticket/tickets.html', {'system_name': 'Document Tracker System', 'user': user,'Category': co, 'Users':users, 'count':count, 'open': openticket})

@login_required(login_url='/')
def search_ticket(request):
  category_filter = request.GET.get('ticket_search_filters')
  search = request.GET.get('seach_ticket')
  co = Category.objects.all()
  ticket = Ticket.objects.filter(category=category_filter,subject__istartswith=search)
  count = Ticket.objects.filter(flag=True,assign_user_id=request.session['userID'] ).count()
  user = User.objects.get(id=request.session['userID'])
  return render(request, './ticket/home.html', {'Ticket': ticket,'Category': co, 'system_name': 'Document Tracker System', 'user': user,'count':count})

@login_required(login_url='/')
def view_profile(request, pk):
  employee = Employee.objects.get(user_id=pk)
  count = Ticket.objects.filter(flag=True,assign_user_id=request.session['userID'] ).count()
  user = User.objects.get(id=request.session['userID'])
  return render(request, './employee_profile.html', {'system_name': 'Document Tracker System', 'user': user,'employee':employee, 'count':count})

@login_required(login_url='/')
def save_ticket(request):
  ticket_edit = request.POST.get('ticket_edit')
  subjects = request.POST.get('ticket_subject')
  description = request.POST.get('description')
  assign_user = request.POST.get('user_choose')
  category = request.POST.get('category_choose')
  requestor = request.POST.get('requestor_choose')
  created_user = request.session['userID']
  stat = request.POST.get('status_choose')
  
  if ticket_edit == '':
     if Ticket.objects.filter(user_requestor_id=requestor,category_id=category,assign_user_id=assign_user).exists() and Ticket.objects.filter(subject=subjects):
       return HttpResponseRedirect('/openticket/')
     else:
       c = Comment(comment='Ticket opened by'+ request.session['name'] )
       ticket = Ticket(subject= subjects, description=description, user_requestor_id=requestor,status=1,flag=1,priority=2,category_id=category,created_by_id=created_user,assign_user_id=assign_user)
       ticket.save()
       t=Ticket.objects.latest('id')
       ticket_age= TicketAge(assign_user_id=assign_user, ticket_id=t.id, done=True)
       ticket_age.save()
       ticket = Ticket.objects.get(created_by_id=created_user,subject=subjects,category_id=category)
       c = Comment(comment='Ticket opened by '+ request.session['name']+' on '+ str(ticket.created), user_id = created_user, ticket_id=ticket.id)
       c.save()  
       return HttpResponseRedirect('/')
  else:
    if Ticket.objects.filter(id=ticket_edit).exists():
     ticket = Ticket.objects.get(id=ticket_edit)
     if ticket.subject != subjects:
       c = Comment(comment='User '+ request.session['name']+' made change(s): New Subject "'+ subjects + '" Old Subject: "'+ticket.subject+'".', user_id = created_user, ticket_id=ticket.id)
       Ticket.objects.filter(id=ticket_edit).update(subject=subjects, flag=True)
       c.save()
     if ticket.description != description:
       c = Comment(comment='User '+ request.session['name']+' made change(s): New Description "'+ description+ '" Old Description "'+ticket.description+'".', user_id = created_user, ticket_id=ticket.id)
       Ticket.objects.filter(id=ticket_edit).update(description=description, flag=True)
       c.save()
     if ticket.user_requestor_id != int(requestor):
       user = User.objects.get(id=requestor)
       c = Comment(comment='User '+ request.session['name']+' made change(s): New Requestor "'+ user.get_full_name() + '" Old Requestor "'+ticket.user_requestor.get_full_name()+'".', user_id = created_user, ticket_id=ticket.id)
       Ticket.objects.filter(id=ticket_edit).update(user_requestor=requestor, flag=True)
       c.save()
     if ticket.category_id != int(category):
        cat = Category.objects.get(id=category)
        c = Comment(comment='User '+ request.session['name']+' made change(s): New Category "'+ cat.name + '" Old Category "'+ticket.category.name+'".', user_id = created_user, ticket_id=ticket.id)
        Ticket.objects.filter(id=ticket_edit).update(category=category, flag=True)
        c.save()  
     if ticket.assign_user_id != int(assign_user):
       user = User.objects.get(id=assign_user)
       TicketAge.objects.filter(ticket_id=ticket_edit).update(modified=datetime.datetime.now(), done=False)
       t=TicketAge(assign_user_id=assign_user,ticket_id=ticket_edit, done=True)
       t.save()
       c = Comment(comment='User '+ request.session['name']+' made change(s): New Assign User "'+ user.get_full_name() + '" Old Assign User "'+ticket.assign_user.get_full_name()+'".', user_id = created_user, ticket_id=ticket.id)
       Ticket.objects.filter(id=ticket_edit).update(assign_user=assign_user, flag=True)
       c.save()
     if ticket.status!=False and stat == 'Close':
       c = Comment(comment='User '+ request.session['name']+' made change(s): Status Open to Close.', user_id = created_user, ticket_id=ticket.id)
       Ticket.objects.filter(id=ticket_edit).update(status=0, flag=True)
       c.save()
     if ticket.status!=True and stat == 'Open':
       c = Comment(comment='User '+ request.session['name']+' made change(s): Status Close to Open.', user_id = created_user, ticket_id=ticket.id)
       Ticket.objects.filter(id=ticket_edit).update(status=1, flag=True)
       c.save()
     return HttpResponseRedirect('/ticketdetailed/'+ticket_edit+'/')
     

@login_required(login_url='/')
def view_ticket(request, pk):
  open_button=True
  form = DocumentForm()
  t = Ticket.objects.get(id=pk)
  query="Select *, justify_hours(age(now(),created)) AS hours FROM tickets_ticketage Where ticket_id="+pk+" and done=True and assign_user_id="+str(t.assign_user_id)
  ticket_age=TicketAge.objects.raw(query)
 
  if request.session['userID'] == t.assign_user_id:  
    Ticket.objects.filter(id=pk).update(flag=False)
  c = Comment.objects.filter(ticket_id=pk).order_by('-created')
  document = Document.objects.filter(ticket_id=pk)
  count = Ticket.objects.filter(flag=True, assign_user_id=request.session['userID']).count()
  user = User.objects.get(id=request.session['userID'])
  return render(request,'./ticket/tickets.html', {'system_name': 'Document Tracker System','ticket': t,'user': user, 'Comment':c, 'count':count, 'com_button':open_button, 'form': form, 'documents': document, 'ticket_age':ticket_age})

@login_required(login_url='/')
def edit_ticket(request, pk):
  edit_open=True
  co = Category.objects.all()
  users = User.objects.all()
  form = DocumentForm()
  t = Ticket.objects.get(id=pk)
  if request.session['userID'] == t.assign_user_id:  
    Ticket.objects.filter(id=pk).update(flag=False)
  c = Comment.objects.filter(ticket_id=pk).order_by('-created')
  document = Document.objects.filter(ticket_id=pk)
  count = Ticket.objects.filter(flag=True, assign_user_id=request.session['userID']).count()
  user = User.objects.get(id=request.session['userID'])
  return render(request,'./ticket/tickets.html', {'system_name': 'Document Tracker System','ticket': t,'user': user, 'Category': co, 'Users':users,'Comment':c, 'count':count,'open':edit_open,'form': form, 'documents': document})

@login_required(login_url='/')
def view_notification(request):
  t = Ticket.objects.filter(assign_user_id=request.session['userID'])
  count = Ticket.objects.filter(flag=True, assign_user_id=request.session['userID']).count()
  user = User.objects.get(id=request.session['userID'])
  return render(request,'./ticket/notification.html', {'system_name': 'Document Tracker System','ticket': t,'user': user, 'count':count})

def view_request(request):
  t = Ticket.objects.filter(user_requestor_id=request.session['userID'])
  count = Ticket.objects.filter(flag=True, assign_user_id=request.session['userID']).count()
  user = User.objects.get(id=request.session['userID'])
  return render(request,'./ticket/notification.html', {'system_name': 'Document Tracker System','ticket': t,'user': user, 'count':count})


@login_required(login_url='/')
def set_comment(request):
    context = RequestContext(request)
    com = request.GET.get('_comment')
    ticket_id = request.GET.get('_ticket')
    c=Comment.objects.create(comment=com,user_id=request.session['userID'], ticket_id = ticket_id)
    c.save()
    co=Comment.objects.filter(ticket_id=ticket_id).order_by('-created')
    #ss='<div> <h1>'+com+'</h1></div>'
    #return HttpResponse(s)  
    return render_to_response('ticket/comment_detail.html', {'Comment': co}, context)

@login_required(login_url='/')
def tickets_assign(request,pk):
  t = Ticket.objects.filter(assign_user_id=pk)
  count = Ticket.objects.filter(flag=True, assign_user_id=request.session['userID']).count()
  user = User.objects.get(id=request.session['userID'])
  return render(request,'./ticket/notification.html', {'system_name': 'Document Tracker System','ticket': t,'user': user, 'count':count})

@login_required(login_url='/')
def tickets_request(request,pk):
  t = Ticket.objects.filter(user_requestor_id=pk)
  count = Ticket.objects.filter(flag=True, assign_user_id=request.session['userID']).count()
  user = User.objects.get(id=request.session['userID'])
  return render(request,'./ticket/notification.html', {'system_name': 'Document Tracker System','ticket': t,'user': user, 'count':count})

def upload(request,pk):
    # Handle file upload

    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        lis = request.FILES['docfile'].name
        if form.is_valid():

            
            newdoc = Document(docfile = request.FILES['docfile'],name=lis,ticket_id=pk, user_id=request.session['userID'])
            c=Comment.objects.create(comment='Uploaded file '+lis,user_id=request.session['userID'], ticket_id = pk)
            newdoc.save()
            c.save()
            
    return HttpResponseRedirect('/ticketdetailed/'+pk+'/')

