from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView, ListView, CreateView, DetailView, DeleteView, UpdateView
from view_breadcrumbs import DetailBreadcrumbMixin, ListBreadcrumbMixin, CreateBreadcrumbMixin, DeleteBreadcrumbMixin, \
    UpdateBreadcrumbMixin
from modules.forms.modules_form import ModulesForm
from modules.models import ModuleModel, CourseModel


class ModeratorView(PermissionRequiredMixin, TemplateView):
    template_name = 'moderator_page.html'
    permission_required = 'accounts.can_view_admin_panel'


class ModulesListView(ListBreadcrumbMixin, PermissionRequiredMixin, ListView):
    model = ModuleModel
    template_name = 'modules/modules_list.html'
    context_object_name = 'modules'
    ordering = ("-create_at",)
    home_path = reverse_lazy('modules:moderator_page')

    def has_permission(self):
        user = self.request.user
        return user.groups.filter(name='moderators').exists() or user.is_superuser


class ModuleCreateView(CreateBreadcrumbMixin, PermissionRequiredMixin, CreateView):
    template_name = "modules/module_create.html"
    model = ModuleModel
    form_class = ModulesForm
    home_path = reverse_lazy('modules:moderator_page')

    def has_permission(self):
        user = self.request.user
        return user.groups.filter(name='moderators').exists() or user.is_superuser

    def get_success_url(self):
        return reverse("modules:modulemodel_list")


class ModuleDetailView(DetailBreadcrumbMixin, PermissionRequiredMixin, DetailView):
    model = ModuleModel
    context_object_name = 'module'
    template_name = 'modules/module_detail.html'
    home_path = reverse_lazy('modules:moderator_page')

    def has_permission(self):
        user = self.request.user
        return user.groups.filter(name='moderators').exists() or user.is_superuser

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['courses'] = CourseModel.objects.filter(module_id=self.object.id)
        return context


class ModuleUpdateView(UpdateBreadcrumbMixin, PermissionRequiredMixin, UpdateView):
    model = ModuleModel
    form_class = ModulesForm
    context_object_name = 'module'
    template_name = 'modules/module_update.html'
    home_path = reverse_lazy('modules:moderator_page')

    def has_permission(self):
        user = self.request.user
        return user.groups.filter(name='moderators').exists() or user.is_superuser

    def get_success_url(self):
        return reverse("modules:modulemodel_list")


class ModuleDeleteView(DeleteBreadcrumbMixin, PermissionRequiredMixin, DeleteView):
    model = ModuleModel
    template_name = "modules/module_delete.html"
    context_object_name = 'module'
    success_url = reverse_lazy("modules:modulemodel_list")
    home_path = reverse_lazy('modules:moderator_page')

    def has_permission(self):
        user = self.request.user
        return user.groups.filter(name='moderators').exists() or user.is_superuser
