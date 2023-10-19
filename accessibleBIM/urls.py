"""accessibleBIM URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from allauth.urls import provider_urlpatterns
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns

from accessibleBIM import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('rosetta/', include('rosetta.urls')),
    path('captcha/', include('captcha.urls')),
    path('accounts/social/', include('allauth.socialaccount.urls')),
    path('accounts/', include(provider_urlpatterns)),
] + i18n_patterns(
    path("i18n/", include("django.conf.urls.i18n")),
    path('', include('modules.urls')),
    path('', include('progress.urls')),
    path('', include('accounts.urls')),
    path('', include('step.urls')),
    path('', include('subscription.urls')),
    path('quiz_bim/', include('quiz_bim.urls')),
    path('summernote/', include('django_summernote.urls')),
    path('statistics/', include('reports.urls')),
    path('', include('static_pages.urls'))
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
