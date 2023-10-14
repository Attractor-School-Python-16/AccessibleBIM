from django.shortcuts import render
from django.views.generic import TemplateView


class AccessibleBIM(TemplateView):
    template_name = "static_pages/accessible-bim.html"


class About(TemplateView):
    template_name = "static_pages/about.html"


class Contacts(TemplateView):
    template_name = "static_pages/contacts.html"


class PrivacyPolicy(TemplateView):
    template_name = "static_pages/privacy-policy.html"
