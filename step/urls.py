from django.urls import path

from step.views.file_view import FileListView, FileDetailView, FileCreateView, FileUpdateView, FileDeleteView
from step.views.step_view import StepListView, StepDetailView, StepUpdateView, StepDeleteView, StepCreateView
from step.views.text_view import TextListView, TextDetailView, TextCreateView, TextUpdateView, TextDeleteView
from step.views.video_view import VideoListView, VideoDetailView, VideoCreateView, VideoUpdateView, VideoDeleteView

app_name = 'step'

urlpatterns = [
    path('step/<int:pk>/', StepDetailView.as_view(), name='stepmodel_detail'),
    path('step/create/text/', StepCreateView.as_view(), name='stepmodel_text_create'),
    path('step/create/video/', StepCreateView.as_view(), name='stepmodel_video_create'),
    path('step/create/quiz/', StepCreateView.as_view(), name='stepmodel_quiz_create'),
    path('step/<int:pk>/update/', StepUpdateView.as_view(), name='stepmodel_update'),
    path('step/<int:pk>/delete/', StepDeleteView.as_view(), name='stepmodel_delete'),

    path('videos/', VideoListView.as_view(), name='videomodel_list'),
    path('video/<int:pk>/', VideoDetailView.as_view(), name='videomodel_detail'),
    path('video/create/', VideoCreateView.as_view(), name='videomodel_create'),
    path('video/<int:pk>/update/', VideoUpdateView.as_view(), name='videomodel_update'),
    path('video/<int:pk>/delete/', VideoDeleteView.as_view(), name='videomodel_delete'),

    path('texts/', TextListView.as_view(), name='textmodel_list'),
    path('text/<int:pk>/', TextDetailView.as_view(), name='textmodel_detail'),
    path('text/create/', TextCreateView.as_view(), name='textmodel_create'),
    path('text/<int:pk>/update/', TextUpdateView.as_view(), name='textmodel_update'),
    path('text/<int:pk>/delete/', TextDeleteView.as_view(), name='textmodel_delete'),

    path('files/', FileListView.as_view(), name='filemodel_list'),
    path('file/<int:pk>/', FileDetailView.as_view(), name='filemodel_detail'),
    path('file/create/', FileCreateView.as_view(), name='filemodel_create'),
    path('file/<int:pk>/update/', FileUpdateView.as_view(), name='filemodel_update'),
    path('file/<int:pk>/delete/', FileDeleteView.as_view(), name='filemodel_delete')
]
