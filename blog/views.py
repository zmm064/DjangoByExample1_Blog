from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail
from django.views.generic import ListView
from .forms import EmailPostForm, CommentForm
from .models import Post, Comment
from taggit.models import Tag
from django.db.models import Count


def post_list(request, tag_slug=None):
    posts = Post.published.all()
    tag = None
    # 根据标签筛选文章
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        #Since this is a many-to-many relationship, 
        #we have to filter by tags contained in a given list, 
        #which in our case contains only one element.
        posts = posts.filter(tags__in=[tag])

    # 分页
    paginator = Paginator(posts, 3)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return render(request, 'blog/post/list.html', {'posts':posts, 'tag':tag})


class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'  #  The default variable is object_list
    paginate_by = 3  # Django's ListView passes the selected page in a variable called page_obj
    template_name = 'blog/post/list.html'

def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post, status='published', 
                           publish__year=year, publish__month=month, publish__day=day)
    comments = post.comments.filter(active=True)

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
    else:
        comment_form = CommentForm()

    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    # 对相似的博文进行排序并取前四项
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags','-publish')[:4]

    return render(request, 'blog/post/detail.html', {
            'post': post, # 发布的文章
            'comments': comments, # 相关评论
            'comment_form': comment_form, # 评论表单
            'similar_posts': similar_posts,
        })


def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False

    if request.method == 'POST':
        form = EmailPostForm(request.POST) # 填充好数据的表单
        if form.is_valid():
            cd = form.cleaned_data
            # 生成URL的绝对地址
            post_url = request.build_absolute_uri(post.get_absolute_url())
            # ... send email
            subject = f"{cd['name']} ({cd['email']}) recommends you reading {post.title}"
            message = f"Read {post.title} at {post_url}\n\n{cd['name']}\'s comments: {cd['comments']}"
            send_mail(subject, message, '1542904808@qq.com', [cd['to']], fail_silently=False)
            sent = True
    else:
        form = EmailPostForm() # 空表单
    return render(request, 'blog/post/share.html', {'post': post, 'form': form, 'sent': sent})