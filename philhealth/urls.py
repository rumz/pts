from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth.views import login, logout
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required

from tickets.views import ( 
	set_comment, 
	ticketing_login, 
	open_ticket,
	save_ticket,
    view_ticket,
    view_notification,
    search_ticket,
    view_profile,
    view_request,
    tickets_assign,
    tickets_request,
    upload,
    edit_ticket,
    about,
    close_status_ticket,
    open_status_ticket,
    all_tickets,
    closed_tickets,
    advance_search,
    advance_search_ticket
	)
# CategoryList, , about, user_login,

admin.autodiscover()


urlpatterns = patterns('',

    url(r'^admin/', include(admin.site.urls)),
    url(r'^comment?$', set_comment),
    url(r'^$',ticketing_login),
    url(r'^notification/$',view_notification),
    url(r'^request/$',view_request),
    url(r'^openticket/$',open_ticket),
    url(r'^save$',save_ticket),
    url(r'^search_ticket?$',search_ticket),
    url(r'^ticketdetailed/(?P<pk>\d+)/$',view_ticket),
    url(r'^edit_ticket/(?P<pk>\d+)/$',edit_ticket),
    url(r'^assign_tickets/(?P<pk>\d+)/$',tickets_assign),
    url(r'^requester_tickets/(?P<pk>\d+)/$',tickets_request),
    url(r'^ticketdetailed/(?P<pk>\d+)/upload/$',upload),
    url(r'^profile/(?P<pk>\d+)/$',view_profile),
    url(r'^close_status_ticket/(?P<pk>\d+)/$',close_status_ticket),
    url(r'^open_status_ticket/(?P<pk>\d+)/$',open_status_ticket),
    url(r'about$',about),
    url(r'alltickets$',all_tickets),
    url(r'closedtickets$',closed_tickets),
    url(r'advance_search$',advance_search),
    url(r'advance_search_ticket?$',advance_search_ticket),
    url(r'^logout/$',logout, {'next_page':'/'} )

)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)