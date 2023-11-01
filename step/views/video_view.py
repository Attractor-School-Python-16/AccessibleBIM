from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView
from view_breadcrumbs import DetailBreadcrumbMixin, ListBreadcrumbMixin, CreateBreadcrumbMixin, DeleteBreadcrumbMixin, \
    UpdateBreadcrumbMixin
from step.forms.video_form import VideoForm
from step.models import VideoModel, StepModel


class VideoListView(ListBreadcrumbMixin, LoginRequiredMixin, ListView):
    model = VideoModel
    template_name = 'steps/video/video_list.html'
    context_object_name = 'videos'
    home_path = reverse_lazy('modules:moderator_page')


class VideoDetailView(DetailBreadcrumbMixin, LoginRequiredMixin, DetailView):
    model = VideoModel
    queryset = VideoModel.objects.all()
    template_name = "steps/video/video_detail.html"
    context_object_name = 'video'
    home_path = reverse_lazy('modules:moderator_page')


class VideoCreateView(CreateBreadcrumbMixin, PermissionRequiredMixin, CreateView):
    model = VideoModel
    form_class = VideoForm
    template_name = "steps/video/video_create.html"
    success_url = reverse_lazy('step:videomodel_list')
    home_path = reverse_lazy('modules:moderator_page')


    def has_permission(self):
        return self.request.user.has_perm('step.add_videomodel')


class VideoUpdateView(UpdateBreadcrumbMixin, PermissionRequiredMixin, UpdateView):
    model = VideoModel
    form_class = VideoForm
    template_name = 'steps/video/video_update.html'
    success_url = reverse_lazy('step:videomodel_list')
    home_path = reverse_lazy('modules:moderator_page')

    def has_permission(self):
        return self.request.user.has_perm('step.change_videomodel')


class VideoDeleteView(DeleteBreadcrumbMixin, PermissionRequiredMixin, DeleteView):
    model = VideoModel
    template_name = 'steps/video/video_delete.html'
    success_url = reverse_lazy('step:videomodel_list')
    home_path = reverse_lazy('modules:moderator_page')
    context_object_name = "video"

    def form_valid(self, form):
        steps = StepModel.objects.all().filter(video=self.object)
        if steps:
            return render(self.request, 'steps/video/video_delete.html', context={
                "form": form,
                "steps": steps,
                "video": self.object
            })
        return super().form_valid(form)

    def has_permission(self):
        return self.request.user.has_perm('step.delete_videomodel')
