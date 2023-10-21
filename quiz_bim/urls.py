from django.urls import path

from quiz_bim.views.answer_bim_views import AnswerBimCreateView, AnswerBimUpdateView, AnswerBimDeleteView
from quiz_bim.views.question_bim_views import QuestionBimCreateView, QuestionBimDetailView, QuestionBimUpdateView, \
    QuestionBimDeleteView
from quiz_bim.views.take_quiz_views import TakeQuizView, QuestionsCompletionView, UserAnswerAPIView, QuizResultView
from quiz_bim.views.quiz_bim_views import QuizBimListView, QuizBimCreateView, QuizBimDetailView, QuizBimUpdateView, \
    QuizBimDeleteView

app_name = 'quiz_bim'

urlpatterns = [
    path('', QuizBimListView.as_view(), name='quizbim_list'),
    path('test/create/', QuizBimCreateView.as_view(), name='quizbim_create'),
    path('test/<int:pk>/', QuizBimDetailView.as_view(), name='quizbim_detail'),
    path('test/<int:pk>/update/', QuizBimUpdateView.as_view(), name='quizbim_update'),
    path('test/<int:pk>/delete/', QuizBimDeleteView.as_view(), name='quizbim_delete'),
    path('test/<int:pk>/question_bim/create/', QuestionBimCreateView.as_view(), name='questionbim_create'),
    path('question_bim/<int:pk>/', QuestionBimDetailView.as_view(), name='questionbim_detail'),
    path('question_bim/<int:pk>/update/', QuestionBimUpdateView.as_view(), name='questionbim_update'),
    path('question_bim/<int:pk>/delete/', QuestionBimDeleteView.as_view(), name='questionbim_delete'),
    path('question_bim/<int:pk>/answer_bim/create/', AnswerBimCreateView.as_view(), name='answerbim_create'),
    path('answer_bim/<int:pk>/update/', AnswerBimUpdateView.as_view(), name='answerbim_update'),
    path('answer_bim/<int:pk>/delete/', AnswerBimDeleteView.as_view(), name='answerbim_delete'),
    path('take-test/<int:pk>/', TakeQuizView.as_view(), name='take_quiz'),
    path('test-completion/<int:pk>/', QuestionsCompletionView.as_view(), name='test_completion'),
    path('api/answer/<int:pk>/', UserAnswerAPIView.as_view(), name='user_answer'),
    path('test-result/<int:pk>/', QuizResultView.as_view(), name='test_result'),
]
