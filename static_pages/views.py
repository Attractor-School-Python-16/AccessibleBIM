from django.shortcuts import render
from django.views.generic import TemplateView


class AccessibleBIM(TemplateView):
    template_name = "static_pages/accessibleBIM.html"
