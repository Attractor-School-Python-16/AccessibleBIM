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
    paginate_by = 5
    courses_buying = None

    def dispatch(self, request, *args, **kwargs):
        self.courses_buying = CourseModel.objects.filter(Q(subscription__is_published=True) & (
                Q(subscription__users=self.request.user) & Q(subscription__us_subscriptions__is_active=True)))
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)
        context['selected_modules'] = self.request.GET.getlist('modules', [])
        context['selected_languages'] = self.request.GET.getlist('languages', [])
        context['selected_targets'] = self.request.GET.getlist('targets', [])
        context['course_targets'] = {data.title: data.title for data in CourseTargetModel.objects.all()}
        context['modules'] = {data.title: data.title for data in ModuleModel.objects.all()}
        context['languages'] = {str(data[0]): str(data[1]) for data in CourseModel.TypeChoices.choices}
        context['courses_buying'] = self.courses_buying
        params = self.get_filter_params()
        query = ''
        if params['modules']:
            for module in params['modules']:
                query += f"modules={module}&"

        if params['languages']:
            for language in params['languages']:
                query += f"languages={language}&"

        if params['targets']:
            for target in params['targets']:
                query += f"targets={target}&"

        context["query"] = query
        try:
            context['user_subscription'] = UsersSubscription.objects.get(Q(user=self.request.user) & Q(is_active=True))
        except UsersSubscription.DoesNotExist:
            context['user_subscription'] = None
        except TypeError:
            context['user_subscription'] = None
        return context

    def get_filter_params(self):
        params = {'modules': self.request.GET.getlist('modules', []),
                  'languages': self.request.GET.getlist('languages', []),
                  'targets': self.request.GET.getlist('targets', [])}
        return params

    def get_queryset(self):
        queryset = CourseModel.objects.exclude(pk=self.courses_buying[0].pk)
        print(queryset)
        print(self.courses_buying)
        params = self.get_filter_params()

        if params['modules']:
            queryset = queryset.filter(module_id__title__in=params['modules'])

        if params['languages']:
            queryset = queryset.filter(language__in=params['languages'])

        if params['targets']:
            queryset = queryset.filter(courseTarget_id__title__in=params['targets'])
        return queryset


class CourseUserDetailView(DetailView):
    model = CourseModel
    context_object_name = 'course'
    template_name = 'front/courses/course_detail.html'
    home_path = reverse_lazy('modules:moderator_page')
    queryset = CourseModel.objects.filter(subscription__price__isnull=False, subscription__is_published=True)

    # Необходимо добавить проверку при просмотре купленного курса, если есть прогресс прохождения, то добавить ссылку
    # перехода на последний шаг.
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['chapters'] = ChapterModel.objects.filter(course=self.object.id)
        context['first_chapter'] = ChapterModel.objects.get(course=self.object.id, serial_number=1)
        subscription = SubscriptionModel.objects.filter(course=self.object)
        if subscription:
            context['subscription'] = subscription[0]
            if self.request.user.is_authenticated:
                user_subscription = UsersSubscription.objects.filter(user=self.request.user,
                                                                     subscription=subscription[0])
                if user_subscription:
                    context['user_subscription'] = user_subscription[0].is_active
        return context

    # def has_permission(self):
    #     course = self.get_object()
    #     return course.subscription.all()
