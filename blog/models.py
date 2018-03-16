from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from taggit.managers import TaggableManager

class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status='published')


class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    author = models.ForeignKey(User, related_name='blog_posts')

    title   = models.CharField(max_length=250)
    slug    = models.SlugField(max_length=250, unique_for_date='publish')
    body    = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status  = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    objects = models.Manager()  # 默认的模型管理器
    published = PublishedManager()  # 自定义的模型管理器
    tags = TaggableManager()

    '''
    >>> post = Post.objects.get(id=1)
    >>> post.tags.add('music', 'jazz', 'django')
    >>> post.tags.all()
        [<Tag: jazz>, <Tag: django>, <Tag: music>]
    >>> post.tags.remove('django')
    >>> post.tags.all()
        [<Tag: jazz>, <Tag: music>]
    '''

    class Meta:
        ordering = ('-publish',)
    
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post_detail', kwargs={
                'year' :self.publish.year,
                'month':self.publish.strftime('%m'),
                'day'  :self.publish.strftime('%d'),
                'post' :self.slug,
            })

class Comment(models.Model):
    post    = models.ForeignKey(Post, related_name='comments')

    name    = models.CharField(max_length=80)
    email   = models.EmailField()
    body    = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active  = models.BooleanField(default=True)
    
    class Meta:
        ordering = ('created',)

    def __str__(self):
        return f'Comment by {self.name} on {self.post}'