from django.shortcuts import render

from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import Topic, Entry
from .forms import TopicForm, EntryForm

from datetime import datetime


# Create your views here.
def index(request):
    """Домашняя страница приложения apple"""
    # request.session.set_test_cookie()

    response = render(request, 'apple/index.html')
    visits = int(request.COOKIES.get('visits', '0'))
    context = {'visits': visits}
    response = render(request, 'apple/index.html', context)
    # if request.COOKIES.keys() in ['last_visit']:
    #     last_visit = request.COOKIES['last_visit']
    #     # last_visit_time = datetime.strptime(last_visit[:-7], "%Y-%m-%d %H:%M:%S")
    #
    #     # if (datetime.now() - last_visit_time).days < 100:
    #     #    response.set_cookie('last_visit', datetime.now())
    #
    # response.set_cookie('visits', visits + 1)

    # else:
    #     response.set_cookie('last_visit', datetime.now())

    if request.session.get('last_visit'):
        last_visit_time = request.session.get('last_visit')
        visits = request.session.get('visits', 0)
        request.session['visits'] = visits + 1
        request.session['last_visit'] = str(datetime.now())
    else:
        request.session['visits'] = 1
        request.session['last_visit'] = str(datetime.now())
    return response


@login_required
def topics(request):
    """Список тем"""
    # if request.session.test_cookie_worked():
    #     print(">>>It's Worked!!!")
    #     request.session.delete_test_cookie()
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    context = {'topics': topics}
    return render(request, 'apple/topics.html', context)


def check_topic_owner(request, id):
    topic = Topic.objects.get(id=id)
    if topic.owner != request.user:
        raise Http404


@login_required
def topic(request, topic_id):
    """ВСе записи одной темы"""
    topic = Topic.objects.get(id=topic_id)
    check_topic_owner(request, topic_id)
    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 'entries': entries}
    return render(request, 'apple/topic.html', context)


@login_required
def new_topic(request):
    if request.method != 'POST':
        # Данные не отправлялись; создается пустая форма.
        form = TopicForm()
    else:
        # Отправлены данные POST; обработать данные.
        form = TopicForm(request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return HttpResponseRedirect(reverse('apple:topics'))

    context = {'form': form}
    return render(request, 'apple/new_topic.html', context)


@login_required
def new_entry(request, topic_id):
    topic = Topic.objects.get(id=topic_id)
    check_topic_owner(request, topic_id)
    if request.method != "POST":
        form = EntryForm()
    else:
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return HttpResponseRedirect(reverse('apple:topic', args=[topic_id]))

    context = {'form': form, 'topic': topic}
    return render(request, 'apple/new_entry.html', context)


@login_required
def edit_entry(request, entry_id):
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    check_topic_owner(request, entry_id)

    if request.method != "POST":
        form = EntryForm(instance=entry)
    else:
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('apple:topic', args=[topic.id]))

    context = {'form': form, 'topic': topic, 'entry': entry}
    return render(request, 'apple/edit_entry.html', context)