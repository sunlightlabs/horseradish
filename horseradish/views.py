from django.views.generic.base import TemplateView


class HelpView(TemplateView):
    template_name = "help.html"
