from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.shortcuts import  render
from .models import ModelCV,RequestLog



class CVDetailView(DetailView):
    model = ModelCV
    template_name = 'main/template_detail.html'
    context_object_name = 'cv'


class CVListView(ListView):
    model = ModelCV
    template_name = 'main/template_list.html'
    context_object_name = 'cvs'

def recent_requests(request):
    logs = RequestLog.objects.values(
        "http_method", "path", "timestamp").order_by("-timestamp")[:10]
    return render(
        request,
        "main/request_log_list.html",
        {"logs": logs}
    )
    
def settings_view(request):
    return render(request, "main/template_settings.html")