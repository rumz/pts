from django.contrib import admin
from tickets.models import TimeStampedModel
from tickets.models import User
from tickets.models import Employee
from tickets.models import Ticket
from tickets.models import Comment


class EmployeeAdmin(admin.ModelAdmin):
    model = Employee
    list_display = ['full_name', 'user', 'position', 'department']
    search_fields = ['user']


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 2


class TicketAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['subject', 'description', 'requester', 'status',
                                         'priority', 'category', 'created_by', 'assigned']}),
    ]
    inlines = [CommentInline]
    list_display = ['id', 'subject', 'description', 'requester', 'assigned']

    list_filter = ['created']
    search_fields = ['subject', 'description']


admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Ticket, TicketAdmin)
