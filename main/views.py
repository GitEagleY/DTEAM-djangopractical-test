from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from .models import ModelCV


class CVDetailView(DetailView):
    model = ModelCV
    template_name = 'main/template_detail.html'
    context_object_name = 'cv'


class CVListView(ListView):
    model = ModelCV
    template_name = 'main/template_list.html'
    context_object_name = 'cvs'
