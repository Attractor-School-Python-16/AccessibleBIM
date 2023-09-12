from django.urls import path

from progress.views.progress_test_answers_view import ProgressTestAnswersCreateView, ProgressTestAnswersDeleteView

app_name = 'progress'

urlpatterns = [
    # path('create/', ProgressTestAnswersCreateView.as_view(), name='create_progress_test'),
    path('<int:pk>/delete/', ProgressTestAnswersDeleteView.as_view(), name='delete_progress_test'),

]
