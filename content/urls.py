from django.urls import path

from content.views import ListPartnersView, AddPartnerView, UpdatePartnerView, DeletePartnerView

app_name = 'content'

urlpatterns = [
    path('partners/', ListPartnersView.as_view(), name='partners_list'),
    path('partners/add/', AddPartnerView.as_view(), name='add_partner'),
    path('partners/<int:pk>/update/', UpdatePartnerView.as_view(), name='update_partner'),
    path('partners/<int:pk>/delete/', DeletePartnerView.as_view(), name='delete_partner'),
]
