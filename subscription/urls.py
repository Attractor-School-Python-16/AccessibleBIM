from django.urls import path

from subscription.views.subscription import SubscriptionListView, SubscriptionCreateView, SubscriptionDeleteView, \
    SubscriptionDetailView, SubscriptionUpdateView, SubscriptionUserListView, SubscriptionUserAddView, SubscriptionUserDeleteView

app_name = 'subscription'

urlpatterns = [
    path('subscription/', SubscriptionListView.as_view(), name="subscription_list"),
    path('subscription/create/', SubscriptionCreateView.as_view(), name="subscription_create"),
    path('subscription/<int:pk>/detail/', SubscriptionDetailView.as_view(), name="subscription_detail"),
    path('subscription/<int:pk>/update/', SubscriptionUpdateView.as_view(), name="subscription_update"),
    path('subscription/<int:pk>/delete/', SubscriptionDeleteView.as_view(), name="subscription_delete"),
    path('subscription/users_list/', SubscriptionUserListView.as_view(), name="subscription_users_list"),
    path('subscription/user_add/<int:pk>/', SubscriptionUserAddView.as_view(), name="subscription_user_add"),
    path('subscription/user_delete/<int:pk>/', SubscriptionUserDeleteView.as_view(), name="subscription_user_delete"),
]
