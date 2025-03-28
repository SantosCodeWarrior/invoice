from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = patterns('',
	url(r'^$', 'it.views.login_user', name='login_user'),
    url(r'^it/', include('it.urls')),
     url(r'^it/', include('it.invoice_urls')),
	#url(r'^$', 'it.views.index', name='index'), 
    url(r'^admin/', include(admin.site.urls)),   
)+static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
