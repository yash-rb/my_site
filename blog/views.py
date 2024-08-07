from django.shortcuts import render, get_object_or_404
from .models import Post, Comment
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from .forms import EmailPostForm, CommentForm
from django.core.mail import send_mail
from django.views.decorators.http import require_POST

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
    
     #Adding Error handling in List view
    def get(self, request, *args, **kwargs):
        paginator = Paginator(self.queryset, self.paginate_by)

        page_number = request.GET.get('page', 1)
        try:
            page_obj = paginator.page(page_number)
        except PageNotAnInteger:
            # If page is not an integer, deliver the first page.
            page_obj = paginator.page(1)
        except EmptyPage:
            # If the page is out of range, deliver the last page of results.
            page_obj = paginator.page(paginator.num_pages)

        context = {
            'posts':page_obj.object_list,
            'page_obj': page_obj,
            'paginator': paginator,
            'is_paginated': paginator.num_pages > 1,}
        
        return render(request, self.template_name, context)
    
   

def post_detail(request, year, month, day, post):
    
    #This method will handle the error and generate a HTTP 404 (not found) exception if oject is not found" 
    post = get_object_or_404(Post, status=Post.Status.PUBLISHED,
                             slug=post,
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    # List of active comments for this post
    comments = post.comments.filter(active=True)
    # Form for users to comment
    form = CommentForm()

    return render(request, 'blog/post/detail.html',
                  {'post':post,
                   'comments':comments,
                   'form':form}) 

def post_share(request, post_id):
    post = get_object_or_404(Post, id = post_id, status=Post.Status.PUBLISHED)
    sent = False
    if request.method == 'POST':
        #It means form is submited
        form = EmailPostForm(request.POST)
        
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommends read {post.title}" 
            message= f"Read {post.title} @ {post_url}\n\n"\
                f"{cd['name']}\s comments: {cd['comments']} "
            send_mail(subject, message, "yashraj78289@gmail.com",[cd['to']])
            sent = True  
    else :
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post':post, 'form':form, 'sent':sent})
    
@require_POST    
def post_comment(request, post_id):
    print("Recieved post")
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    comment = None
    form = CommentForm(data=request.POST)
    if form.is_valid():
        print("is_valid")
        
         # Create a Comment object without saving it to the database
        comment = form.save(commit=False)
        # Assign the post to the comment
        comment.post = post
        # SAve the comment to the database
        
        comment.save()
        return render(request, 'blog/post/comment.html', 
                      {'post':post,
                       'form':form,
                       'comment':comment
                       })
    else: print(form.errors)
