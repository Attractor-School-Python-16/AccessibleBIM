from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView

from step.forms.step_form import StepForm
from step.forms.video_form import VideoForm
from step.models import VideoModel


class VideoListView(ListView):
    model = VideoModel
    template_name = 'video/video_list.html'
    context_object_name = 'videos'


class VideoDetailView(DetailView):
    queryset = VideoModel.objects.all()
    template_name = "video/video_detail.html"


class VideoCreateView(CreateView):
    form_class = VideoForm
    template_name = "video/video_create.html"


class VideoUpdateView(UpdateView):
    model = VideoModel
    form_class = StepForm
    template_name = 'video/video_update.html'
    success_url = reverse_lazy('video_list')


class VideoDeleteView(DeleteView):
    model = VideoModel
    template_name = 'video/video_delete.html'
    success_url = reverse_lazy('video_list')