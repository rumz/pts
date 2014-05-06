import os
import sys

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

# Start execution here!
if __name__ == '__main__':
    print "Starting Tickets population script..."
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'philhealth.settings')
    from tickets.models import Category
    populate()
