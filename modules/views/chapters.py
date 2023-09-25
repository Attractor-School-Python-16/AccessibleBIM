import re

from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import ListView, CreateView, DetailView, DeleteView, UpdateView

from modules.forms.chapters_form import ChaptersForm
from modules.models import ChapterModel, CourseModel
from step.models import StepModel


class ChaptersListView(PermissionRequiredMixin, ListView):
    model = ChapterModel
    template_name = 'chapters/chapters_list.html'
    context_object_name = 'chapters'
    ordering = ("-create_at",)

    def has_permission(self):
        user = self.request.user
        return user.groups.filter(name='moderators').exists() or user.is_superuser


class ChapterCreateView(PermissionRequiredMixin, CreateView):
    template_name = "chapters/chapter_create.html"
    model = ChapterModel
    form_class = ChaptersForm
    course = None

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
        return reverse("modules:chapter_detail", kwargs={"pk": self.object.pk})


class ChapterDetailView(PermissionRequiredMixin, DetailView):
    model = ChapterModel
    context_object_name = 'chapter'
    template_name = 'chapters/chapter_detail.html'

    def has_permission(self):
        user = self.request.user
        return user.groups.filter(name='moderators').exists() or user.is_superuser

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['steps'] = StepModel.objects.filter(chapter=self.object.id)
        return context


class ChapterUpdateView(PermissionRequiredMixin, UpdateView):
    model = ChapterModel
    form_class = ChaptersForm
    context_object_name = 'chapter'
    template_name = 'chapters/chapter_update.html'

    def has_permission(self):
        user = self.request.user
        return user.groups.filter(name='moderators').exists() or user.is_superuser

    def get_success_url(self):
        return reverse("modules:chapter_detail", kwargs={"pk": self.object.pk})


class ChapterDeleteView(PermissionRequiredMixin, DeleteView):
    model = ChapterModel
    template_name = "chapters/chapter_delete.html"
    context_object_name = 'chapter'
    success_url = reverse_lazy("modules:chapters_list")

    def has_permission(self):
        user = self.request.user
        return user.groups.filter(name='moderators').exists() or user.is_superuser


class ChapterChangeStepsOrderView(PermissionRequiredMixin, View):
    template_name = 'courses/change_steps_order.html'

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
        course = get_object_or_404(CourseModel, pk=kwargs['pk'])

        new_serial_numbers = {}
        for key, value in request.POST.items():
            if key.startswith('new_serial_number_'):
                chapter_number = int(re.search(r'\d+', key).group())
                new_serial_numbers[chapter_number] = int(re.search(r'\d+', value).group())

        chapters = ChapterModel.objects.filter(course=course)
        unique_numbers = set(new_serial_numbers.values())

        if len(unique_numbers) < len(new_serial_numbers):
            messages.error(request, 'Выберите разные порядковые номера для глав.')
        else:
            for chapter_id, new_number in new_serial_numbers.items():
                chapter = chapters.get(pk=chapter_id)
                chapter.serial_number = new_number
                chapter.save()

        return redirect('modules:course_detail', pk=course.pk)
