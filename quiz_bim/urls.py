from django.urls import path

from quiz_bim.views.answer_bim_views import AnswerBimCreateView, AnswerBimUpdateView, AnswerBimDeleteView
from quiz_bim.views.question_bim_views import QuestionBimCreateView, QuestionBimDetailView, QuestionBimUpdateView, \
    QuestionBimDeleteView
from quiz_bim.views.take_test_views import TakeTestView, QuestionsCompletionView, UserAnswerAPIView, TestResultView
from quiz_bim.views.test_bim_views import TestsBimListView, TestBimCreateView, TestBimDetailView, TestBimUpdateView, \
    TestBimDeleteView

app_name = 'quiz_bim'

urlpatterns = [
    path('', TestsBimListView.as_view(), name='tests_list'),
    path('test/create/', TestBimCreateView.as_view(), name='test_create'),
    path('test/<int:pk>/', TestBimDetailView.as_view(), name='test_detail'),
    path('test/<int:pk>/update/', TestBimUpdateView.as_view(), name='test_update'),
    path('test/<int:pk>/delete/', TestBimDeleteView.as_view(), name='test_delete'),
    path('test/<int:pk>/question_bim/create/', QuestionBimCreateView.as_view(), name='question_create'),
    path('question_bim/<int:pk>/', QuestionBimDetailView.as_view(), name='question_detail'),
    path('question_bim/<int:pk>/update/', QuestionBimUpdateView.as_view(), name='question_update'),
    path('question_bim/<int:pk>/delete/', QuestionBimDeleteView.as_view(), name='question_delete'),
    path('question_bim/<int:pk>/answer_bim/create/', AnswerBimCreateView.as_view(), name='answer_create'),
    path('answer_bim/<int:pk>/update/', AnswerBimUpdateView.as_view(), name='answer_update'),
    path('answer_bim/<int:pk>/delete/', AnswerBimDeleteView.as_view(), name='answer_delete'),
    path('take-test/<int:pk>/', TakeTestView.as_view(), name='take_test'),
    path('test-completion/<int:pk>/', QuestionsCompletionView.as_view(), name='test_completion'),
    path('api/answer/<int:pk>', UserAnswerAPIView.as_view(), name='user_answer'),
    path('test-result/<int:pk>', TestResultView.as_view(), name='test_result'),
]
