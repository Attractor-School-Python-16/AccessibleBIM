from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView, ListView, CreateView, DetailView, DeleteView, UpdateView

from modules.forms.modules_form import ModulesForm
from modules.models import ModuleModel, CourseModel


class HomeView(TemplateView):
    template_name = 'index.html'


class ModeratorView(PermissionRequiredMixin, TemplateView):
    template_name = 'moderator_page.html'

    def has_permission(self):
        return self.request.user.groups.filter(name='moderators').exists()


class ModulesListView(PermissionRequiredMixin, ListView):
    model = ModuleModel
    template_name = 'modules/modules_list.html'
    context_object_name = 'modules'
    ordering = ("-create_at",)

    def has_permission(self):
        user = self.request.user
        return user.groups.filter(name='moderators').exists() or user.is_superuser


class ModuleCreateView(PermissionRequiredMixin, CreateView):
    template_name = "modules/module_create.html"
    model = ModuleModel
    form_class = ModulesForm

    def has_permission(self):
        user = self.request.user
        return user.groups.filter(name='moderators').exists() or user.is_superuser

    def get_success_url(self):
        return reverse("modules:module_detail", kwargs={"pk": self.object.pk})


class ModuleDetailView(PermissionRequiredMixin, DetailView):
    model = ModuleModel
    context_object_name = 'module'
    template_name = 'modules/module_detail.html'

    def has_permission(self):
        user = self.request.user
        return user.groups.filter(name='moderators').exists() or user.is_superuser

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['courses'] = CourseModel.objects.filter(module_id=self.object.id)
        return context


class ModuleUpdateView(PermissionRequiredMixin, UpdateView):
    model = ModuleModel
    form_class = ModulesForm
    context_object_name = 'module'
    template_name = 'modules/module_update.html'

    def has_permission(self):
        user = self.request.user
        return user.groups.filter(name='moderators').exists() or user.is_superuser

    def get_success_url(self):
        return reverse("modules:module_detail", kwargs={"pk": self.object.pk})


class ModuleDeleteView(PermissionRequiredMixin, DeleteView):
    model = ModuleModel
    template_name = "modules/module_delete.html"
    context_object_name = 'module'
    success_url = reverse_lazy("modules:modules_list")

    def has_permission(self):
        user = self.request.user
        return user.groups.filter(name='moderators').exists() or user.is_superuser


class StepVideoView(TemplateView):
    template_name = 'steps/step_detail_video.html'


class StepTextView(TemplateView):
    template_name = 'steps/step_detail_text.html'


class StepFileView(TemplateView):
    template_name = 'steps/step_detail_file.html'


class QuizDetailView(TemplateView):
    template_name = 'quiz_bim/quiz_bim_detail.html'
