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
from django.views.i18n import JavaScriptCatalog

from accessibleBIM import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('rosetta/', include('rosetta.urls')),
    path('captcha/', include('captcha.urls')),
    path('accounts/', include('allauth.urls')),
    path('accounts/social/', include('allauth.socialaccount.urls')),
    path('accounts/', include(provider_urlpatterns)),
] + i18n_patterns(
    path("i18n/", include("django.conf.urls.i18n")),
    path('', include('front.urls')),
    path('', include('accounts.urls')),
    path('moderator/', include('modules.urls')),
    path('moderator/', include('progress.urls')),
    path('moderator/', include('step.urls')),
    path('moderator/', include('subscription.urls')),
    path('quiz_bim/', include('quiz_bim.urls')),
    path('summernote/', include('django_summernote.urls')),
    path('statistics/', include('reports.urls')),
    path('moderator/', include('content.urls')),
    path("jsi18n/", JavaScriptCatalog.as_view(), name="javascript-catalog"),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = "front.views.errors_handler.page_not_found_view"
handler403 = "front.views.errors_handler.permission_denied_view"
handler500 = "front.views.errors_handler.server_error_view"
