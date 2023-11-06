from django.urls import path

from content.views import ListPartnersView, PartnerDetailView, AddPartnerView, UpdatePartnerView, DeletePartnerView

app_name = 'content'

urlpatterns = [
    path('partners/', ListPartnersView.as_view(), name='partners_list'),
    path('partners/<int:pk>/', PartnerDetailView.as_view(), name='partner_detailed'),
    path('partners/add/', AddPartnerView.as_view(), name='add_partner'),
    path('partners/update/', UpdatePartnerView.as_view(), name='update_partner'),
    path('partners/delete/', DeletePartnerView.as_view(), name='delete_partner'),
]
