from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import Topic, Entry
from .forms import TopicForm, EntryForm


# Create your views here.
def index(request):
    """The homepage of the LearnLogs"""
    return render(request, 'LearnLogs/index.html')


@login_required
def topics(request):
    """The page shows all the topics"""
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    context = {'topics': topics}
    return render(request, 'LearnLogs/topics.html', context)


@login_required
def topic(request, topic_id):
    """The page shows one topic and its all entries """
    topic = Topic.objects.get(id=topic_id)
    if topic.owner != request.user:
        raise Http404

    entries = topic.entry_set.order_by('-date_added')
    context = {
        'topic': topic,
        'entries': entries,
    }
    return render(request, 'LearnLogs/topic.html', context)


@login_required
def new_topic(request):
    """The page is used to add new topic"""
    if request.method != 'POST':
        # No submitted datas, create a new form
        form = TopicForm()
    else:
        # progress with the posted datas
        form = TopicForm(request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return HttpResponseRedirect(reverse('LearnLogs:topics'))

    context = {'form': form}
    return render(request, 'LearnLogs/new_topic.html', context)


@login_required
def new_entry(request, topic_id):
    """The page is used to add a new entry for a topic"""
    topic = Topic.objects.get(id=topic_id)

    if request.method != 'POST':
        # No submitted datas, create a new form
        form = EntryForm()
    else:
        form = EntryForm(request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return HttpResponseRedirect(
                reverse('LearnLogs:topic', args=[topic_id]))

    context = {'topic': topic, 'form': form}
    return render(request, 'LearnLogs/new_entry.html', context)


@login_required
def edit_entry(request, entry_id):
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    if topic.owner != request.user:
        raise Http404

    if request.method != 'POST':
        form = EntryForm(instance=entry)
    else:
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(
                reverse('LearnLogs:topic', args=[topic.id]))

    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'LearnLogs/edit_entry.html', context)
