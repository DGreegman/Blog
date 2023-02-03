from django.shortcuts import render, get_object_or_404
from .models import Post, Comment
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from .forms import EmailPostForm, CommentForm
from django.core.mail import send_mail
from django.views.decorators.http import require_POST
# Create your views here.

# def post_list(request):
#     post_list = Post.published.all()
#     # Pagination with 3 posts per page
#     paginator = Paginator(post_list, 3)
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
    # model = Post
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = "blog/post/list.html"


def post_detail(request, year, month, day, post):
    
    # try:
    #     post = Post.published.get(id=id)
    # except Post.DoesNotExist:
    #     raise Http404("No Post Found")
    
    post = get_object_or_404(Post, status=Post.Status.PUBLISHED, 
                            slug=post,
                            publish__year=year,
                            publish__month=month,
                            publish__day=day)

    # list of all active comment for this post
    comments = post.comments.filter(active=True)
    # form for users to comment
    form = CommentForm()

    return render(request, 'blog/post/detail.html', 
                            {'post': post,
                            'comments': comments,
                            'form':form})

# for sharing of post using email 
def post_share(request, post_id):
    
    #retrieve post by id
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    sent = False

    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} Recommends You Read "\
                      f"{post.title}"
            message = f"Read {post.title} at {post_url}\n\n"\
                      f"{cd['name']}\'s Comments: {cd['comments']}"
            send_mail(subject, message, 'obeagug@gmail.com', [cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'form': form, 'post': post, 'sent': sent})


# function to post comment in a form
@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED) 
    comment = None
    # a comment was posted
    form = CommentForm(data=request.POST)
    if form.is_valid():
        # create a comment object without saving it to the database
        comment = form.save(commit=False)
        # assign the post to the comment
        comment.post = post
        # save the post the databse
        comment.save()
    return render(request, 'blog/post/comment.html', {
        'post': post,
        'form': form,
        'comment': comment
    })