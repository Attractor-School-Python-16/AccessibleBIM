import re
from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils.functional import cached_property
from django.views import View
from django.views.generic import ListView, CreateView, DetailView, DeleteView, UpdateView
from view_breadcrumbs import DetailBreadcrumbMixin, ListBreadcrumbMixin, CreateBreadcrumbMixin, DeleteBreadcrumbMixin, \
    UpdateBreadcrumbMixin
from modules.forms.courses_form import CoursesForm
from modules.models import CourseModel, ModuleModel, ChapterModel, CourseTargetModel
from subscription.models import SubscriptionModel
from subscription.models.user_subscription import UsersSubscription


class CoursesListView(ListBreadcrumbMixin, PermissionRequiredMixin, ListView):
    model = CourseModel
    template_name = 'courses/courses_list.html'
    context_object_name = 'courses'
    ordering = ("-create_at",)
    home_path = reverse_lazy('modules:moderator_page')

    def has_permission(self):
        user = self.request.user
        return user.groups.filter(name='moderators').exists() or user.is_superuser


class CoursesUserListView(ListView):
    model = CourseModel
    template_name = 'courses/courses_user_list.html'
    context_object_name = 'courses'
    ordering = "-create_at"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['selected_modules'] = self.request.GET.getlist('modules', [])
        context['selected_languages'] = self.request.GET.getlist('languages', [])
        context['selected_targets'] = self.request.GET.getlist('targets', [])
        context['course_targets'] = CourseTargetModel.objects.all()
        context['modules'] = ModuleModel.objects.all()
        return context

    def get_queryset(self):
        queryset = CourseModel.objects.filter(subscription__price__isnull=False, subscription__is_published=True)
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


class CourseCreateView(CreateBreadcrumbMixin, PermissionRequiredMixin, CreateView):
    template_name = "courses/course_create.html"
    model = CourseModel
    form_class = CoursesForm
    module_pk = None
    home_path = reverse_lazy('modules:moderator_page')

    def has_permission(self):
        user = self.request.user
        return user.groups.filter(name='moderators').exists() or user.is_superuser

    def get_initial(self):
        self.module_pk = self.request.GET.get('module_pk')
        return {'module_id': self.module_pk}

    def form_valid(self, form):
        form.instance.module_id = ModuleModel.objects.get(id=self.module_pk)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("modules:modulemodel_detail", kwargs={"pk": self.object.module_id.pk})


class CourseDetailView(DetailBreadcrumbMixin, PermissionRequiredMixin, DetailView):
    model = CourseModel
    context_object_name = 'course'
    template_name = 'courses/course_detail.html'
    home_path = reverse_lazy('modules:moderator_page')

    @cached_property
    def crumbs(self):
        course = self.get_object()
        module = self.get_object().module_id
        chapter = course.ct_course.first()

        return [
            (module._meta.verbose_name_plural, reverse_lazy("modules:modulemodel_list")),
            (module.title, reverse_lazy("modules:modulemodel_detail", kwargs={"pk": module.pk})),
            (course.title, reverse_lazy("modules:modulemodel_detail", kwargs={"pk": course.module_id.pk})),
        ]

    def has_permission(self):
        user = self.request.user
        return user.groups.filter(name='moderators').exists() or user.is_superuser

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['chapters'] = ChapterModel.objects.filter(course=self.object.id)
        return context


class CourseUserDetailView(DetailView):
    model = CourseModel
    context_object_name = 'course'
    template_name = 'courses/course_user_detail.html'
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
                user_subscription = UsersSubscription.objects.filter(user=self.request.user, subscription=subscription[0])
                if user_subscription:
                    context['user_subscription'] = user_subscription[0].is_active
        return context


class CourseUpdateView(UpdateBreadcrumbMixin, PermissionRequiredMixin, UpdateView):
    model = CourseModel
    form_class = CoursesForm
    context_object_name = 'course'
    template_name = 'courses/course_update.html'
    home_path = reverse_lazy('modules:moderator_page')

    @cached_property
    def crumbs(self):
        module = self.get_object().module_id

        return [
            (module._meta.verbose_name_plural, reverse_lazy("modules:modulemodel_list")),
            (module.title, reverse_lazy("modules:modulemodel_detail", kwargs={"pk": module.pk}))
        ] + super().crumbs

    def has_permission(self):
        user = self.request.user
        return user.groups.filter(name='moderators').exists() or user.is_superuser

    def get_success_url(self):
        return reverse("modules:modulemodel_detail", kwargs={"pk": self.object.module_id.pk})


class CourseDeleteView(DeleteBreadcrumbMixin, PermissionRequiredMixin, DeleteView):
    model = CourseModel
    template_name = "courses/course_delete.html"
    context_object_name = 'course'
    home_path = reverse_lazy('modules:moderator_page')

    @cached_property
    def crumbs(self):
        module = self.get_object().module_id

        return [
            (module._meta.verbose_name_plural, reverse_lazy("modules:modulemodel_list")),
            (module.title, reverse_lazy("modules:modulemodel_detail", kwargs={"pk": module.pk}))
        ] + super().crumbs


    def has_permission(self):
        user = self.request.user
        return user.groups.filter(name='moderators').exists() or user.is_superuser

    def get_success_url(self):
        return reverse("modules:modulemodel_detail", kwargs={"pk": self.object.module_id.pk})


class CourseChangeChaptersOrderView(PermissionRequiredMixin, View):
    template_name = 'courses/change_chapters_order.html'

    def has_permission(self):
        user = self.request.user
        return user.groups.filter(name='moderators').exists() or user.is_superuser

    def get(self, request, *args, **kwargs):
        course = CourseModel.objects.get(pk=kwargs['pk'])
        chapters = ChapterModel.objects.filter(course=course)
        context = {
            'course': course,
            'chapters': chapters,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        course = get_object_or_404(CourseModel, pk=kwargs['pk'])
        data = self.request.POST
        new_serial_numbers = {}
        for i in data:
            if "pk" in i:
                chapter_id = i.split("_")[1]
                new_serial_numbers[chapter_id] = data[i]
        chapters = ChapterModel.objects.filter(course=course)
        unique_numbers = set(new_serial_numbers.values())
        if len(unique_numbers) < len(new_serial_numbers):
            messages.error(request, 'Выберите разные порядковые номера для глав.')
        else:
            for chapter_id, new_number in new_serial_numbers.items():
                chapter = chapters.get(id=chapter_id)
                chapter.serial_number = new_number
                chapter.save()
        return redirect('modules:coursemodel_detail', pk=course.pk)
