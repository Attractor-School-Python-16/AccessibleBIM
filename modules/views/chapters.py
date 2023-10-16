import re

from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.utils.functional import cached_property
from django.views import View
from django.views.generic import ListView, CreateView, DetailView, DeleteView, UpdateView
from view_breadcrumbs import DetailBreadcrumbMixin, ListBreadcrumbMixin, CreateBreadcrumbMixin, DeleteBreadcrumbMixin, \
    UpdateBreadcrumbMixin
from modules.forms.chapters_form import ChaptersForm
from modules.models import ChapterModel, CourseModel
from step.models import StepModel

# ChaptersListView здесь создана только для работы DetailBreadcrumbMixin, т.к. он наследуется от ListBreadcrumbMixin и
# без него не работают хлебные крошки.
class ChaptersListView(ListBreadcrumbMixin, PermissionRequiredMixin, ListView):
    model = ChapterModel
    template_name = 'chapters/chapters_list.html'
    context_object_name = 'chapters'
    ordering = ("-create_at",)
    home_path = reverse_lazy('modules:moderator_page')

    def has_permission(self):
        user = self.request.user
        return user.groups.filter(name='moderators').exists() or user.is_superuser


class ChapterCreateView(CreateBreadcrumbMixin, PermissionRequiredMixin, CreateView):
    template_name = "chapters/chapter_create.html"
    model = ChapterModel
    form_class = ChaptersForm
    course = None
    home_path = reverse_lazy('modules:moderator_page')

    def has_permission(self):
        user = self.request.user
        return user.groups.filter(name='moderators').exists() or user.is_superuser

    def get_initial(self):
        self.course = self.request.GET.get('course_pk')
        return {'course': self.course}

    def form_valid(self, form):
        form.instance.course = CourseModel.objects.get(id=self.course)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("modules:coursemodel_detail", kwargs={"pk": self.object.course.pk})


class ChapterDetailView(DetailBreadcrumbMixin, PermissionRequiredMixin, DetailView):
    model = ChapterModel
    context_object_name = 'chapter'
    template_name = 'chapters/chapter_detail.html'
    home_path = reverse_lazy('modules:moderator_page')

    @cached_property
    def crumbs(self):
        chapter = self.get_object()
        course = chapter.course
        module = course.module_id


        return [
            (module._meta.verbose_name_plural, reverse_lazy("modules:modulemodel_list")),
            (module.title, reverse_lazy("modules:modulemodel_detail", kwargs={"pk": module.pk})),
            (course.title, reverse_lazy("modules:coursemodel_detail", kwargs={"pk": chapter.course.pk})),
            (chapter.title, reverse_lazy("modules:chaptermodel_detail", kwargs={"pk": chapter.pk})),
        ]

    def has_permission(self):
        user = self.request.user
        return user.groups.filter(name='moderators').exists() or user.is_superuser

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['steps'] = StepModel.objects.filter(chapter=self.object.id)
        return context

    def get_success_url(self):
        return reverse("modules:coursemodel_detail", kwargs={"pk": self.object.course.pk})


class ChapterUpdateView(UpdateBreadcrumbMixin, PermissionRequiredMixin, UpdateView):
    model = ChapterModel
    form_class = ChaptersForm
    context_object_name = 'chapter'
    template_name = 'chapters/chapter_update.html'
    home_path = reverse_lazy('modules:moderator_page')

    @cached_property
    def crumbs(self):
        course = self.get_object().course
        module = course.module_id

        return [
            (module._meta.verbose_name_plural, reverse_lazy("modules:modulemodel_list")),
            (module.title, reverse_lazy("modules:modulemodel_detail", kwargs={"pk": module.pk})),
            (course.title, reverse_lazy("modules:coursemodel_detail", kwargs={"pk": course.pk})),
        ] + super().crumbs

    def has_permission(self):
        user = self.request.user
        return user.groups.filter(name='moderators').exists() or user.is_superuser

    def get_success_url(self):
        return reverse("modules:coursemodel_detail", kwargs={"pk": self.object.course.pk})


class ChapterDeleteView(DeleteBreadcrumbMixin, PermissionRequiredMixin, DeleteView):
    model = ChapterModel
    template_name = "chapters/chapter_delete.html"
    context_object_name = 'chapter'
    success_url = reverse_lazy("modules:chapters_list")
    home_path = reverse_lazy('modules:moderator_page')

    @cached_property
    def crumbs(self):
        course = self.get_object().course
        module = course.module_id

        return [
            (module._meta.verbose_name_plural, reverse_lazy("modules:modulemodel_list")),
            (module.title, reverse_lazy("modules:modulemodel_detail", kwargs={"pk": module.pk})),
            (course.title, reverse_lazy("modules:coursemodel_detail", kwargs={"pk": course.pk})),
        ] + super().crumbs

    def has_permission(self):
        user = self.request.user
        return user.groups.filter(name='moderators').exists() or user.is_superuser

    def get_success_url(self):
        return reverse("modules:coursemodel_detail", kwargs={"pk": self.object.course.pk})

    def form_valid(self, form):
        step = self.get_object()
        course = step.course
        response = super().form_valid(form)
        self.update_serial_numbers(course)
        return response

    def update_serial_numbers(self, course):
        chapters = ChapterModel.objects.filter(course=course).order_by('serial_number')
        current_serial_number = 1
        for chapter in chapters:
            if chapter.serial_number != current_serial_number:
                chapter.serial_number = current_serial_number
                chapter.save()
            current_serial_number += 1


class ChapterChangeStepsOrderView(PermissionRequiredMixin, View):
    template_name = 'chapters/change_steps_order.html'

    def has_permission(self):
        user = self.request.user
        return user.groups.filter(name='moderators').exists() or user.is_superuser

    def get(self, request, *args, **kwargs):
        chapter = ChapterModel.objects.get(pk=kwargs['pk'])
        steps = StepModel.objects.filter(chapter=chapter)
        context = {
            'chapter': chapter,
            'steps': steps,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        chapter = get_object_or_404(ChapterModel, pk=kwargs['pk'])
        new_serial_numbers = {}
        for key, value in request.POST.items():
            if key.startswith('new_serial_number_'):
                step_id = int(re.search(r'\d+', key).group())
                new_serial_numbers[step_id] = int(re.search(r'\d+', value).group())

        steps = StepModel.objects.filter(chapter=chapter)
        unique_numbers = set(new_serial_numbers.values())

        if len(unique_numbers) < len(new_serial_numbers):
            messages.error(request, 'Выберите разные порядковые номера для глав.')
        else:
            for step_id, new_number in new_serial_numbers.items():
                step = steps.get(id=step_id)
                step.serial_number = new_number
                step.save()

        return redirect('modules:chaptermodel_detail', pk=kwargs['pk'])
