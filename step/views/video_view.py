from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView


from step.forms.video_form import VideoForm
from step.models import VideoModel


class VideoListView(LoginRequiredMixin, ListView):
    model = VideoModel
    template_name = 'steps/video/video_list.html'
    context_object_name = 'videos'


class VideoDetailView(LoginRequiredMixin, DetailView):
    queryset = VideoModel.objects.all()
    template_name = "steps/video/video_detail.html"
    context_object_name = 'video'


class VideoCreateView(PermissionRequiredMixin, CreateView):
    form_class = VideoForm
    template_name = "steps/video/video_create.html"

    def has_permission(self):
        return self.request.user.has_perm('step.add_videomodel')


class VideoUpdateView(UpdateView):
    model = VideoModel
    form_class = VideoForm
    template_name = 'steps/video/video_update.html'
    success_url = reverse_lazy('step:video_list')


class VideoDeleteView(DeleteView):
    model = VideoModel
    template_name = 'steps/video/video_delete.html'
    success_url = reverse_lazy('step:video_list')
