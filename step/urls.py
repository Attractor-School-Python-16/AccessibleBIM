from django.urls import path

from step.views.step_view import StepListView, StepDetailView, StepUpdateView, StepDeleteView, StepCreateView
from step.views.text_view import TextListView, TextDetailView, TextCreateView, TextUpdateView, TextDeleteView
from step.views.video_view import VideoListView, VideoDetailView, VideoCreateView, VideoUpdateView, VideoDeleteView

app_name = 'step'

urlpatterns = [
    path('steps/', StepListView.as_view(), name='step_list'),
    path('step/<int:pk>/', StepDetailView.as_view(), name='step_detail'),
    path('step/create/', StepCreateView.as_view(), name='step_create'),
    path('step/<int:pk>/update/', StepUpdateView.as_view(), name='step_update'),
    path('step/<int:pk>/delete/', StepDeleteView.as_view(), name='step_delete'),
    path('videos/', VideoListView.as_view(), name='video_list'),
    path('video/<int:pk>/', VideoDetailView.as_view(), name='video_detail'),
    path('video/create/', VideoCreateView.as_view(), name='video_create'),
    path('video/<int:pk>/update/', VideoUpdateView.as_view(), name='video_update'),
    path('video/<int:pk>/delete/', VideoDeleteView.as_view(), name='video_delete'),
    path('texts/', TextListView.as_view(), name='text_list'),
    path('video/<int:pk>/', TextDetailView.as_view(), name='text_detail'),
    path('video/create/', TextCreateView.as_view(), name='text_create'),
    path('video/<int:pk>/update/', TextUpdateView.as_view(), name='text_update'),
    path('video/<int:pk>/delete/', TextDeleteView.as_view(), name='text_delete')
]
