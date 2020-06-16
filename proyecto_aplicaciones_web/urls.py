import django
from django.apps import apps
from django.conf import settings
from django.conf.urls import include, url, re_path
from django.urls import include, path
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.conf.urls import include
from django.contrib import admin
from django.contrib.sitemaps import views
from oscar.views import handler403, handler404, handler500

from apps.sitemaps import base_sitemaps

from django.views.generic.base import TemplateView

from wagtail.admin import urls as wagtailadmin_urls
from wagtail.core import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls


admin.autodiscover()

urlpatterns = [
    # Include admin as convenience. It's unsupported and only included
    # for developers.
    url(r'^admin/', admin.site.urls),

    # i18n URLS need to live outside of i18n_patterns scope of Oscar
    url(r'^i18n/', include(django.conf.urls.i18n)),
    #url(r'^$', views.index, name='index'),
    url(r'^gadifishing', TemplateView.as_view(template_name='home.html'), name='inicio'),
    
 url(r'^checkout/paypal/', include('paypal.express.urls')),
    # Dashboard views for Payflow Pro
    url(r'^dashboard/paypal/payflow/', apps.get_app_config("payflow_dashboard").urls),
    # Dashboard views for Express
    url(r'^dashboard/paypal/express/', apps.get_app_config("express_dashboard").urls),
    
    path('AppGF/', include('AppGF.urls')),
    path('', include('AppGF.urls')),

    url(r'^cms/', include(wagtailadmin_urls)),
    url(r'^documents/', include(wagtaildocs_urls)),

    url(r'^blog/', include(wagtail_urls), name='inicio_blog'),

    # include a basic sitemap
    url(r'^sitemap\.xml$', views.index,
        {'sitemaps': base_sitemaps}),
    url(r'^sitemap-(?P<section>.+)\.xml$', views.sitemap,
        {'sitemaps': base_sitemaps},
        name='django.contrib.sitemaps.views.sitemap')
]

# Prefix Oscar URLs with language codes
urlpatterns += i18n_patterns(
    url(r'^', include(apps.get_app_config('oscar').urls[0])),
)

if settings.DEBUG:
    import debug_toolbar

    # Server statics and uploaded media
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # Allow error pages to be tested
    urlpatterns += [
        url(r'^403$', handler403, {'exception': Exception()}),
        url(r'^404$', handler404, {'exception': Exception()}),
        url(r'^500$', handler500),
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]
