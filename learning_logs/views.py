from django.shortcuts import render, redirect
from .models import Topic
from .forms import TopicForm, EntryForm


# Create your views here.
def index(request):
    """The homepage for learning log"""
    return render(request, 'learning_logs/index.html')


def topics(request):
    """show all topics"""
    topics_available = Topic.objects.order_by('date_added')
    context = {
        "topics": topics_available
    }
    return render(request, 'learning_logs/topics.html', context)


def topic(request, topic_id):
    """show a given topic and all its associated entries"""
    given_topic = Topic.objects.get(id=topic_id)
    entries = given_topic.entry_set.order_by('-date_added')
    context = {"topic": given_topic, "entries": entries}
    return render(request, 'learning_logs/topic.html', context)


def new_topic(request):
    """Add a new topic"""
    if request.method != 'POST':
        # No data submitted, create a blank form
        form = TopicForm()
    else:
        # POST data submitted, process data
        form = TopicForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('learning_logs:topics')

    # Display a blank or invalid form
    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)


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
