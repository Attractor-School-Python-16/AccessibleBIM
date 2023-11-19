from django.urls import path

from content.views import ListPartnersView, AddPartnerView, UpdatePartnerView, DeletePartnerView
from content.views.team_member_view import ListTeamView, AddTeamView, UpdateTeamView, DeleteTeamView

app_name = 'content'

urlpatterns = [
    path('partners/', ListPartnersView.as_view(), name='partners_list'),
    path('partners/add/', AddPartnerView.as_view(), name='add_partner'),
    path('partners/<int:pk>/update/', UpdatePartnerView.as_view(), name='update_partner'),
    path('partners/<int:pk>/delete/', DeletePartnerView.as_view(), name='delete_partner'),
    path('team/', ListTeamView.as_view(), name='team_list'),
    path('team/add/', AddTeamView.as_view(), name='add_team'),
    path('team/<int:pk>/update/', UpdateTeamView.as_view(), name='update_team'),
    path('team/<int:pk>/delete/', DeleteTeamView.as_view(), name='delete_team'),
]
