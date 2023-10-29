from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView

from modules.models import CourseModel, CourseTargetModel, ModuleModel, ChapterModel
from subscription.models import SubscriptionModel
from subscription.models.user_subscription import UsersSubscription


class CoursesUserListView(ListView):
    model = CourseModel
    template_name = 'front/courses/courses.html'
    context_object_name = 'courses'
    ordering = "-create_at"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['selected_modules'] = self.request.GET.getlist('modules', [])
        context['selected_languages'] = self.request.GET.getlist('languages', [])
        context['selected_targets'] = self.request.GET.getlist('targets', [])
        context['course_targets'] = CourseTargetModel.objects.all()
        context['modules'] = ModuleModel.objects.all()
        try:
            context['user_subscription'] = UsersSubscription.objects.get(Q(user=self.request.user) & Q(is_active=True))
        except UsersSubscription.DoesNotExist:
            context['user_subscription'] = None
        return context

    def get_queryset(self):
        queryset = CourseModel.objects.all()
        modules = self.request.GET.getlist('modules', [])
        languages = self.request.GET.getlist('languages', [])
        targets = self.request.GET.getlist('targets', [])

        if modules:
            queryset = queryset.filter(module_id__title__in=modules)

        if languages:
            queryset = queryset.filter(language__in=languages)

        if targets:
            queryset = queryset.filter(courseTarget_id__title__in=targets)
        return queryset


class CourseUserDetailView(DetailView):
    model = CourseModel
    context_object_name = 'course'
    template_name = 'front/courses/course_detail.html'
    home_path = reverse_lazy('modules:moderator_page')

    # Необходимо добавить проверку при просмотре купленного курса, если есть прогресс прохождения, то добавить ссылку
    # перехода на последний шаг.
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['chapters'] = ChapterModel.objects.filter(course=self.object.id)
        context['first_chapter'] = ChapterModel.objects.get(course=self.object.id, serial_number=1)
        if self.request.user.is_authenticated:
            subscription = SubscriptionModel.objects.filter(course=self.object)
            if subscription:
                context['subscription'] = subscription[0]
                user_subscription = UsersSubscription.objects.filter(user=self.request.user,
                                                                     subscription=subscription[0])
                if user_subscription:
                    context['user_subscription'] = user_subscription[0].is_active
        return context

    # def has_permission(self):
    #     course = self.get_object()
    #     return course.subscription.all()
