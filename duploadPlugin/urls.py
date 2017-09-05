from django.conf.urls import include, url

from django.contrib import admin
from plugin import urls as plugin_urls
admin.autodiscover()

urlpatterns = [
    # Examples:
    # url(r'^$', 'duploadPlugin.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'', include(plugin_urls)),
]
