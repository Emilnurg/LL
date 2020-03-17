import os


def populate():
    python_cat = add_cat("Python")

    add_entry(topic=python_cat,
              text='Python Tutorial',
              url="http://docs.python.org/2/tutorial/")

    for c in Topic.objects.all():
        for e in Entry.objects.filter():
            print("- {0} - {1}".format(str(c), str(e)))


def add_entry(topic, text, url, views=0):
    p = Entry.objects.get_or_create(topic=topic, text=text, url=url, views=views)[0]
    return p


def add_cat(text):
    c = Topic.objects.get_or_create(text=text)[0]
    return c


# Start execution
if __name__ == '__main':
    print("Startuem")
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'learning_logs.settings')
    from apple.models import Entry, Topic
    populate()
