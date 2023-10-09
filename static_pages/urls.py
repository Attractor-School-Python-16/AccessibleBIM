from django.urls import path

from static_pages.views import AccessibleBIM

app_name = 'static_pages'

urlpatterns = [
    path("accessible-bim/", AccessibleBIM.as_view(), name="accessible_bim"),
]