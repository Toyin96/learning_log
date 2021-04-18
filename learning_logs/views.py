from django.shortcuts import render, redirect
from .models import Topic, Entry
from .forms import TopicForm, EntryForm
from django.contrib.auth.decorators import login_required
from django.http import Http404


# Create your views here.
def index(request):
    """The homepage for learning log"""
    return render(request, 'learning_logs/index.html')


@login_required
def topics(request):
    """show all topics"""
    topics_available = Topic.objects.filter(owner=request.user).order_by('date_added')
    context = {
        "topics": topics_available
    }
    return render(request, 'learning_logs/topics.html', context)


@login_required
def topic(request, topic_id):
    """show a given topic and all its associated entries"""
    # Make sure the topic belong to one owner
    given_topic = Topic.objects.get(id=topic_id)

    if given_topic.owner != request.user:
        raise Http404

    entries = given_topic.entry_set.order_by('-date_added')
    context = {"topic": given_topic, "entries": entries}
    return render(request, 'learning_logs/topic.html', context)


@login_required
def new_topic(request):
    """Add a new topic"""
    if request.method != 'POST':
        # No data submitted, create a blank form
        form = TopicForm()
    else:
        # POST data submitted, process data
        form = TopicForm(data=request.POST)
        if form.is_valid():
            created_topic = form.save(commit=False)
            created_topic.owner = request.user
            created_topic.save()
            return redirect('learning_logs:topics')

    # Display a blank or invalid form
    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)


@login_required
def new_entry(request, topic_id):
    """Adds a new entry for a particular topic"""
    topic = Topic.objects.get(id=topic_id)

    if request.method != 'POST':
        # No data submitted; create a blank form.
        form = EntryForm()
    else:
        # POST data submitted; process data.
        form = EntryForm(data=request.POST)
        new_entry = form.save(commit=False)
        new_entry.topic = topic
        new_entry.save()

    # Displays an empty or invalid form
    context = {'topic': topic, 'form': form}
    return render(request, 'learning_logs/new_entry.html', context)


@login_required
def edit_entry(request, entry_id):
    """Edit an existing entry"""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic

    if topic.owner != request.user:
        raise Http404

    # Initial request, prefill form with the current entry
    if request.method != 'POST':
        form = EntryForm(instance=entry)
    else:
        # Post data submitted; process data.
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('learning_logs:topic', topic_id=topic.id)

    context = {
        'entry': entry, 'topic': topic, 'form': form
    }
    return render(request, 'learning_logs/edit_entry.html', context)
