from django.shortcuts import render, get_object_or_404
from .models import Post
from django.core.paginator import Paginator
def post_list(request):
    
    post_list = Post.published.all()
    #Adding pagination to the post list view
    paginator = Paginator(post_list, 2  )
    page_number = request.GET.get('page', 1)
    posts = paginator.page(page_number)
    
    return render(request, 'blog/post/list.html', {'posts':posts})

def post_detail(request, year, month, day, post):
    
    #This method will handle the error and generate a HTTP 404 (not found) exception if oject is not found" 
    post = get_object_or_404(Post, status=Post.Status.PUBLISHED,
                             slug=post,
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)

    return render(request, 'blog/post/detail.html', {'post':post}) 
    