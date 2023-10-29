from django.views.generic import TemplateView


class AccessibleBIM(TemplateView):
    template_name = "front/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = 'AccessibleBIM'
        context['sub_title'] = 'БИМСТАНДАРД'
        return context


class About(TemplateView):
    template_name = "front/about.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = 'O нас'
        return context


class Contacts(TemplateView):
    template_name = "front/contacts.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = 'Свяжитесь с нами'
        return context


class PrivacyPolicy(TemplateView):
    template_name = "front/privacy-policy.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = 'Политика конфиденциальности'
        return context
