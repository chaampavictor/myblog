from __future__ import unicode_literals
from django.shortcuts import render
from django.utils import timezone
from .models import Post
from django.shortcuts import render, get_object_or_404
from blog.forms import PostForm
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from blog.forms import SignupForm


# Create your views here.
def signup(request):
    if request.method == 'POST':
        form= SignupForm(request.POST)
        if form.is_valid():
            user=form.save()
            user.refresh_from_db()
            user.profile.bio = form.cleaned_data['bio']
            user.save()
            #log_user_in
            username = form.cleaned_data['username']
            raw_password = form.cleaned_data['password1']
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('post_list')
    else:
        form=SignupForm()
    return render (request, 'registration/signup.html', {'form' : form})

def post_list(request):
    if request.user.is_authenticated:
        user_posts = Post.objects.filter(published_date__lte=timezone.now(), author=request.user).order_by('published_date')
        other_posts = Post.objects.filter(published_date__lte=timezone.now()).exclude(author=request.user).order_by('published_date')
    else:
        other_posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
        user_posts = None
    return render(request, 'blog/post_list.html', {'other_posts': other_posts, 'user_posts': user_posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

def articles(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    return render(request, 'blog/articles.html', {'posts':posts})


def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})
