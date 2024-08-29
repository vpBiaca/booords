from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login, authenticate
from django.db.models import Count

from .models import Board, Topic, Post
from .forms import TopicForm, PostForm


def home(request):
    boards = Board.objects.all()
    return render(request, 'home.html', {'boards': boards})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('home')
        else:
            error_message = 'Invalid credentials'
    else:
        error_message = ''
    return render(request, 'login.html', {'error_message': error_message})


def board_topics(request, pk):
    boards = get_object_or_404(Board, pk=pk)
    topics = boards.topics.order_by('-last_updated').annotate(replies=Count('posts'))
    return render(request, 'boards/boards.html', {'board': boards, 'topics': topics})


# def new_topic(request, pk):
#     board = get_object_or_404(Board, pk=pk)
#     if request.method == 'POST':
#         form = TopicForm(request.POST)
#         if form.is_valid():
#             topic = form.save(commit=False)
#             topic.board = board
#             topic.starter = request.user
#             topic.save()
#             return redirect('board_topics', pk=board.pk)
#     else:
#         form = TopicForm()
#     return render(request, 'boards/new_topic.html', {'form': form, 'board': board})

def new_topic(request, pk):
    board = get_object_or_404(Board, pk=pk)
    if not request.user.is_authenticated:
        return redirect('login')  # Redirect to the login page if the user is not authenticated
    if request.method == 'POST':
        form = TopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.board = board
            topic.starter = request.user
            topic.save()
            return redirect('board_topics', pk=board.pk)
    else:
        form = TopicForm()
    return render(request, 'boards/new_topic.html', {'form': form, 'board': board})



def topic_posts(request, pk, topic_pk):
    topic = get_object_or_404(Topic, board__pk=pk, pk=topic_pk)
    posts = topic.posts.all()
    topic.views += 1
    topic.save()

    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.topic = topic
            post.created_by = request.user
            post.save()
            return redirect('topic_posts', pk=pk, topic_pk=topic_pk)
    else:
        form = PostForm()
    
    

    return render(request, 'boards/topic_posts.html', {'topic': topic, 'posts': posts, 'form': form})


def new_post(request, pk, topic_pk):
    topic = get_object_or_404(Topic, board__pk=pk, pk=topic_pk)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.topic = topic
            post.created_by = request.user
            post.save()
            return redirect('topic_posts', pk=pk, topic_pk=topic_pk)
    else:
        form = PostForm()
    return render(request, 'boards/new_post.html', {'form': form, 'topic': topic})
