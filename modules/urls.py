from django.urls import path

from modules.views.modules import HomeView, ModulesView, ModulesDetailView

app_name = 'modules'

urlpatterns = [
    path('', HomeView.as_view(), name="index"),
    path('courses/', ModulesView.as_view(), name="modules"),
    path('course/1', ModulesDetailView.as_view(), name="module"), # поменять число на PK
]
