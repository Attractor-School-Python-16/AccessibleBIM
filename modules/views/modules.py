from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = 'index.html'


class ModulesView(TemplateView):
    template_name = 'modules/modules_view.html'


class ModulesDetailView(TemplateView):
    template_name = 'modules/modules_detail.html'
