from django.urls import path

from modules.views.modules import HomeView

urlpatterns = [
    path('', HomeView.as_view(), name="index"),
]
