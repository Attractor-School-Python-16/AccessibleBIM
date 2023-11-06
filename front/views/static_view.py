from django.views.generic import TemplateView


class AccessibleBIM(TemplateView):
    template_name = "front/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = 'Bologna Engineering Excellence'
        return context


# class Old_About(TemplateView):
#     template_name = "front/old_about_page.html"
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data()
#         context['title'] = 'O нас'
#         return context


class About(TemplateView):
    template_name = "front/about.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = 'O нас'
        return context


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
