from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError
from .models import Post
from .forms import PostForm

def post_list(request):
    posts = Post.get_published_posts()
    return render(request, 'blog_app/post_list.html', {'posts': posts})


def post_details(request, pk):
    """
    View single post details.
    View delegates retrieval to model method.
    """
    post = Post.get_post_by_id(pk)
    return render(request, 'blog_app/post_details.html', {'post': post})
 
 
 
def post_create(request):
    """
    Create a new blog post.
    View handles only HTTP request/response and form validation.
    Model handles business logic via create_post() method.
    """
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            try:
                Post.create_post(
                    title=form.cleaned_data['title'],
                    content=form.cleaned_data['content']
                )
                return redirect('post_list')
            except ValidationError as e:
                form.add_error(None, str(e))
    else:
        form = PostForm()
    
    return render(request, 'blog_app/post_form.html', {
        'form': form,
        'action': 'Create'
    })
 
 
 
def post_update(request, pk):
    """
    Update an existing blog post.
    View handles form submission; model handles validation.
    """
    post = Post.get_post_by_id(pk)
    
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            try:
                post.update_post(
                    title=form.cleaned_data['title'],
                    content=form.cleaned_data['content']
                )
                return redirect('post_details', pk=post.pk)
            except ValidationError as e:
                form.add_error(None, str(e))
    else:
        form = PostForm(initial={
            'title': post.title,
            'content': post.content
        })
    
    return render(request, 'blog_app/post_form.html', {
        'form': form,
        'post': post,
        'action': 'Update'
    })
 
 
 
def post_delete(request, pk):
    """
    Delete a blog post.
    View handles confirmation; model handles deletion logic.
    """
    post = Post.get_post_by_id(pk)
    
    if request.method == 'POST':
        post.delete_post()
        return redirect('post_list')
    
    # request.method == 'GET' - show confirmation page
    return render(request, 'blog_app/post_confirm_delete.html', {'post': post})
