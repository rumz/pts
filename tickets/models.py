from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User


class TimeStampedModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class Category(TimeStampedModel):
    name = models.CharField(max_length=128, unique=True)
    description = models.TextField(default='')

    class Meta:
        db_table = 'category'

    def __unicode__(self):
        return self.name


class Employee(models.Model):
    user = models.OneToOneField(User)
    position = models.CharField(max_length=45)
    department = models.CharField(max_length=45)
    address = models.CharField(max_length=100, blank=True)
    image_path = models.FileField(upload_to='profile_pics/', default ='profile_pics/default_male.png')

    class Meta:
        db_table = 'employee'

    def __unicode__(self):
        return self.user.username


class Ticket(TimeStampedModel):
    """
    choice = ((1,'Open'), (0,'Closed'))
    flags  = ((1,'Unread'), (0,'Read'))
    """

    subject = models.CharField(max_length=200)
    description = models.TextField(default='')
    requester = models.ForeignKey(User, related_name = 'requester')
    status = models.BooleanField()
    priority = models.IntegerField()
    category = models.ForeignKey(Category)
    created_by = models.ForeignKey(User, related_name = 'created_by')
    assigned = models.ForeignKey(User, related_name = 'assigned_user')
    flag = models.BooleanField()

    class Meta:
        db_table = 'ticket'

    def __unicode__(self):
        return self.id

    def get_absolute_url(self):
        return reverse('tickets-detail', kwargs={'pk': self.id})


class TicketAge(TimeStampedModel):
    choices=((1,'done'),
            (0,'undone'))
    assign_user = models.ForeignKey(User)
    ticket = models.ForeignKey(Ticket)
    done = models.BooleanField(choices=choices)


class Document(TimeStampedModel):
    ticket = models.ForeignKey(Ticket)
    name = models.CharField(max_length=200)
    docfile = models.FileField(upload_to='documents/%Y/%m/%d')
    user    = models.ForeignKey(User)


class Comment(TimeStampedModel):
    ticket  = models.ForeignKey(Ticket)
    comment = models.TextField()
    user    = models.ForeignKey(User)

    def __unicode__(self):
        return self.comment
