from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, DeleteView, UpdateView

from modules.forms.course_target_form import CourseTargetForm
from modules.models import CourseTargetModel


class CourseTargetsListView(ListView):
    model = CourseTargetModel
    template_name = 'course_target/course_target_list.html'
    context_object_name = 'course_targets'
    ordering = ("-create_at",)


class CourseTargetCreateView(CreateView):
    template_name = "course_target/course_target_create.html"
    model = CourseTargetModel
    form_class = CourseTargetForm

    def get_success_url(self):
        return reverse("modules:course_target_detail", kwargs={"pk": self.object.pk})


class CourseTargetDetailView(DetailView):
    model = CourseTargetModel
    context_object_name = 'course_target'
    template_name = 'course_target/course_target_detail.html'


class CourseTargetUpdateView(UpdateView):
    model = CourseTargetModel
    form_class = CourseTargetForm
    context_object_name = 'course_target'
    template_name = 'course_target/course_target_update.html'

    def get_success_url(self):
        return reverse("modules:course_target_detail", kwargs={"pk": self.object.pk})


class CourseTargetDeleteView(DeleteView):
    model = CourseTargetModel
    template_name = "course_target/course_target_delete.html"
    context_object_name = 'course_target'
    success_url = reverse_lazy("modules:course_targets_list")
