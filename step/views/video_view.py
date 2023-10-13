import os

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView
from view_breadcrumbs import DetailBreadcrumbMixin, ListBreadcrumbMixin, CreateBreadcrumbMixin, DeleteBreadcrumbMixin, \
    UpdateBreadcrumbMixin
from step.forms.video_form import VideoForm
from step.models import VideoModel


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

    def form_valid(self, form):
        form.instance.save(user=self.request.user)
        return super().form_valid(form)


class VideoUpdateView(UpdateBreadcrumbMixin, PermissionRequiredMixin, UpdateView):
    model = VideoModel
    form_class = VideoForm
    template_name = 'steps/video/video_update.html'
    success_url = reverse_lazy('step:videomodel_list')
    home_path = reverse_lazy('modules:moderator_page')

    def has_permission(self):
        return self.request.user.has_perm('step.change_videomodel')


# class VideoDeleteView(DeleteBreadcrumbMixin, PermissionRequiredMixin, DeleteView):
#     model = VideoModel
#     template_name = 'steps/video/video_delete.html'
#     success_url = reverse_lazy('step:videomodel_list')
#     home_path = reverse_lazy('modules:moderator_page')
#
#     def has_permission(self):
#         return self.request.user.has_perm('step.delete_videomodel')


class VideoDeleteView(DeleteBreadcrumbMixin, PermissionRequiredMixin, DeleteView):
    model = VideoModel
    template_name = 'steps/video/video_delete.html'
    success_url = reverse_lazy('step:videomodel_list')
    home_path = reverse_lazy('modules:moderator_page')

    def has_permission(self):
        return self.request.user.has_perm('step.delete_videomodel')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()

        self.remove_related_files(self.object)

        response = super().delete(request, *args, **kwargs)

        return response

    def remove_related_files(self, video_object):
        if video_object.video_file:
            storage, path = video_object.video_file.storage, video_object.video_file.path
            storage.delete(path)

        if video_object.converted_video and video_object.converted_video.video_file:
            storage, path = video_object.converted_video.video_file.storage, video_object.converted_video.video_file.path
            storage.delete(path)

            base_name, ext = os.path.splitext(path)
            conv_path = os.path.join('steps', 'videos', 'conv', f"{base_name}.m3u8")
            thumb_path = os.path.join('steps', 'videos', 'thumb', f"{base_name}.jpg")

            if storage.exists(conv_path):
                storage.delete(conv_path)

            if storage.exists(thumb_path):
                storage.delete(thumb_path)
