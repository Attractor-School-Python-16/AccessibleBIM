from django.urls import path

from step.views.step_view import StepListView, StepDetailView, StepUpdateView, StepDeleteView

app_name = 'step'

urlpatterns = [
    path('steps/', StepListView.as_view(), name='step_list'),
    path('step/<int:pk>/', StepDetailView.as_view(), name='step_detail'),
    path('step/<int:pk>/update/', StepUpdateView.as_view(), name='step_update'),
    path('step/<int:pk>/delete/', StepDeleteView.as_view(), name='step_delete'),
]
