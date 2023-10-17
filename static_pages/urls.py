from django.urls import path

from static_pages.views import AccessibleBIM, About, Contacts, PrivacyPolicy

app_name = 'static_pages'

urlpatterns = [
    path("", AccessibleBIM.as_view(), name="accessible_bim"),
    path("about/", About.as_view(), name="about"),
    path("contacts/", Contacts.as_view(), name="contacts"),
    path("privacy-policy/", PrivacyPolicy.as_view(), name="privacy_policy"),
]