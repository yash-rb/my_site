from django.shortcuts import render, get_object_or_404
from .models import Post
from django.http import Http404

def post_list(request):
    posts = Post.published.all()
    return render(request, 'blog/post/list.html', {'posts':posts})

def post_detail(request, id):
    #This method will handle the error and generate a HTTP 404 (not found) exception if oject is not found" 
    post = get_object_or_404(Post, id=id, status=Post.Status.PUBLISHED)

    return render(request, 'blog/post/detail.html', {'post':post}) 
    