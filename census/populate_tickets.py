import os
import sys
import csv

def populate():
    cat = add_cat('Data Extraction', 'Data Extraction')
    cat = add_cat('Hardware Maintenance', 'Hardware Maintenance')
    cat = add_cat('IT Project', 'IT Project')
    cat = add_cat('Local Support', 'Local Support')
    cat = add_cat('Misc', 'Misc')
    cat = add_cat('Procurement', 'Procurement')
    cat = add_cat('Training', 'Training')

    print "Creating the following: "
    for c in Category.objects.all():
        print "- {0}".format(str(c))


def add_cat(name, description):
    c = Category.objects.get_or_create(name=name, description=description)[0]
    return c


def populate_users():
    """
        extract id numbers, last names, and first names from your old db
        then put them in a file called pts_users.csv in the same directory
        then run this script as you would usually run it
    """

    added_users = []
    allusers = User.objects.all()
    with open('pts_users.csv', 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            (username, last_name, first_name) = row
            if [u.username for u in allusers if u.username == username]:
                print "Existing user: ", \
                                [u.first_name for u in allusers if u.username == username][0]
            else:
                user = User.objects.create_user(username, '', 'xxx123')
                user.last_name = last_name
                user.first_name = first_name
                user.save()
                print "Created user ", user.last_name + ', ' + user.first_name


# Start execution here!
if __name__ == '__main__':
    print "Starting Tickets population script..."
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pts.settings')
    from tickets.models import Category
    populate()

    from django.contrib.auth.models import User
    from django.contrib.auth import authenticate
    populate_users()

