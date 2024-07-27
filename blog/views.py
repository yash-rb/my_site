from django.shortcuts import render, get_object_or_404
from .models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView

# def post_list(request):
    
#     post_list = Post.published.all()
#     #Adding pagination to the post list view
#     paginator = Paginator(post_list, 2  )
#     #if no page specified return first page
#     page_number = request.GET.get('page', 1)
    
#     try:
#         posts = paginator.page(page_number)
        
#     except PageNotAnInteger:
#         # If page_number is not an integer deliver the first page
#         posts = paginator.page(1)
        
#     except EmptyPage:
#         # If page_number is out of range deliver last page of results
#         posts = paginator.page(paginator.num_pages)
    
#     return render(request, 'blog/post/list.html', {'posts':posts})

class PostListView(ListView):
    """
    Alternative post list view
    
    """
    
    queryset = Post.published.all()
    paginate_by = 3
    context_object_name = 'posts'
    template_name = 'blog/post/list.html'
    
   

def post_detail(request, year, month, day, post):
    
    #This method will handle the error and generate a HTTP 404 (not found) exception if oject is not found" 
    post = get_object_or_404(Post, status=Post.Status.PUBLISHED,
                             slug=post,
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)

    return render(request, 'blog/post/detail.html', {'post':post}) 
    