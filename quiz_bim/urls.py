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

    path('test/<int:tpk>/question_bim/detail/<int:qpk>/', QuestionBimFormDetailView.as_view(),
         name='questionbim_htmx_detail'),
    path('test/question_bim/create/', QuestionBimFormCreateView.as_view(), name='questionbim_htmx_create'),
    path('test/<int:tpk>/question_bim/update/<int:qpk>/', QuestionBimFormUpdateView.as_view(),
         name='questionbim_htmx_update'),
    path('test/<int:tpk>/question_bim/delete/<int:qpk>/', QuestionBimFormDeleteView.as_view(),
         name='questionbim_htmx_delete'),

    path('question_bim/<int:qpk>/answer_bim/detail/<int:apk>/', AnswerBimFormDetailView.as_view(),
         name='answerbim_htmx_detail'),
    path('question_bim/<int:pk>/answer_bim/create/', AnswerBimFormCreateView.as_view(), name='answerbim_htmx_create'),
    path('question_bim/<int:qpk>/answer_bim/update/<int:apk>/', AnswerBimFormUpdateView.as_view(),
         name='answerbim_htmx_update'),
    path('question_bim/<int:qpk>/answer_bim/delete/<int:apk>/', AnswerBimFormDeleteView.as_view(),
         name='answerbim_htmx_delete'),

    path('take-test/<int:pk>/', TakeQuizView.as_view(), name='take_quiz'),
    path('test-completion/<int:pk>/', QuestionsCompletionView.as_view(), name='test_completion'),
    path('api/answer/<int:pk>', UserAnswerAPIView.as_view(), name='user_answer'),
    path('test-result/<int:pk>', QuizResultView.as_view(), name='test_result'),
]
