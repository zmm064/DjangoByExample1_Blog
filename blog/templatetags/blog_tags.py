from django import template
from django.db.models import Count

from ..models import Post

register = template.Library()

# define the function as a simple tag and register it
@register.simple_tag
def total_posts():
    return Post.published.count()  # 返回一个字符串


@register.inclusion_tag('blog/post/latest_posts.html')
def show_latest_posts(count=5):
    latest_post = Post.published.order_by('-publish')[:count]
    return {'latest_posts':latest_post}  # 返回一个渲染后的模板


@register.assignment_tag
def get_most_commented_posts(count=5):
    return Post.published.annotate( # 设置上下文中的变量
        total_comments=Count('comments')).order_by('-total_comments')[:count]