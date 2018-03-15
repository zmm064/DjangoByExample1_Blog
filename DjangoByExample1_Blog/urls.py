"""
Definition of urls for DjangoByExample1_Blog.
"""

from django.conf.urls import include, url


from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    # Examples:
    # url(r'^$', DjangoByExample1_Blog.views.home, name='home'),
    # url(r'^DjangoByExample1_Blog/', include('DjangoByExample1_Blog.DjangoByExample1_Blog.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),


    url(r'^admin/', include(admin.site.urls)),
    url(r'^blog/', include('blog.urls', namespace='blog', app_name='blog')),
]
