from duploadPlugin import settings
from django.conf.urls import include, url

from django.contrib import admin
from plugin import urls as plugin_urls
from django.conf.urls.static import static
admin.autodiscover()

urlpatterns = [
    # Examples:
    # url(r'^$', 'duploadPlugin.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'', include(plugin_urls)),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
