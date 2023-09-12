from django.urls import path

from progress.views.progress_test_answers_view import ProgressTestAnswersDeleteView
from progress.views.progress_test_view import ProgressTestDeleteView

app_name = 'progress'

urlpatterns = [
    # path('create/', ProgressTestAnswersCreateView.as_view(), name='create_progress_test'),
    path('<int:pk>/delete/', ProgressTestAnswersDeleteView.as_view(), name='delete_progress_test_answer'),
    path('<int:pk>/delete/', ProgressTestDeleteView.as_view(), name='delete_progress_test'),
]

