import re
from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import ListView, CreateView, DetailView, DeleteView, UpdateView

from modules.forms.courses_form import CoursesForm
from modules.models import CourseModel, ModuleModel, ChapterModel, CourseTargetModel


class CoursesListView(PermissionRequiredMixin, ListView):
    model = CourseModel
    template_name = 'courses/courses_list.html'
    context_object_name = 'courses'
    ordering = ("-create_at",)

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


class CourseCreateView(PermissionRequiredMixin, CreateView):
    template_name = "courses/course_create.html"
    model = CourseModel
    form_class = CoursesForm
    module_pk = None

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
        return reverse("modules:course_detail", kwargs={"pk": self.object.pk})


class CourseDetailView(PermissionRequiredMixin, DetailView):
    model = CourseModel
    context_object_name = 'course'
    template_name = 'courses/course_detail.html'

    def has_permission(self):
        user = self.request.user
        return user.groups.filter(name='moderators').exists() or user.is_superuser

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['chapters'] = ChapterModel.objects.filter(course=self.object.id)
        return context


class CourseUpdateView(PermissionRequiredMixin, UpdateView):
    model = CourseModel
    form_class = CoursesForm
    context_object_name = 'course'
    template_name = 'courses/course_update.html'

    def has_permission(self):
        user = self.request.user
        return user.groups.filter(name='moderators').exists() or user.is_superuser

    def get_success_url(self):
        return reverse("modules:course_detail", kwargs={"pk": self.object.pk})


class CourseDeleteView(PermissionRequiredMixin, DeleteView):
    model = CourseModel
    template_name = "courses/course_delete.html"
    context_object_name = 'course'
    success_url = reverse_lazy("modules:courses_list")

    def has_permission(self):
        user = self.request.user
        return user.groups.filter(name='moderators').exists() or user.is_superuser


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

        new_serial_numbers = {}
        for key, value in request.POST.items():
            if key.startswith('new_serial_number_'):
                chapter_id = int(re.search(r'\d+', key).group())
                new_serial_numbers[chapter_id] = int(re.search(r'\d+', value).group())

        chapters = ChapterModel.objects.filter(course=course)
        unique_numbers = set(new_serial_numbers.values())

        if len(unique_numbers) < len(new_serial_numbers):
            messages.error(request, 'Выберите разные порядковые номера для глав.')
        else:
            for chapter_id, new_number in new_serial_numbers.items():
                chapter = chapters.get(id=chapter_id)
                chapter.serial_number = new_number
                chapter.save()

        return redirect('modules:course_detail', pk=course.pk)
