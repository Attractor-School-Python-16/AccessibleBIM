from django.views.generic import TemplateView

from content.models import PartnerModel, TeamModel


class AccessibleBIM(TemplateView):
    template_name = "front/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = 'Bologna Engineering Excellence'
        context['partners'] = PartnerModel.objects.all()
        return context


class About(TemplateView):
    template_name = "front/about.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = 'O нас'
        context['team'] = TeamModel.objects.all()
        return context


# class Contacts(TemplateView):
#     template_name = "front/contacts.html"
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data()
#         context['title'] = 'Свяжитесь с нами'
#         return context


class PrivacyPolicy(TemplateView):
    template_name = "front/privacy-policy.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = 'Политика конфиденциальности'
        return context


class TermsOfUse(TemplateView):
    template_name = "front/terms_of_use.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        return context
