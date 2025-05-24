from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.shortcuts import  render

from django.http import HttpResponse

from django.shortcuts import get_object_or_404
from django.template.loader import get_template


#from weasyprint import HTML

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

def generate_pdf(request, pk):
    cv = get_object_or_404(ModelCV, id=pk)
    # Use the existing template
    template = get_template("main/template_detail.html")
    html_content = template.render(
        {"object": cv, "pdf_mode": True})  # Pass a flag for styling

    # PDF generation is currently disabled
    # Uncomment the following lines to enable PDF generation
    #pdf_file = HTML(string=html_content).write_pdf()
    #response = HttpResponse(pdf_file, content_type="application/pdf")
    #response["Content-Disposition"] = \
    #    f'attachment; filename="{cv.firstname}_{cv.lastname}_CV.pdf"'

    # Return a simple response indicating PDF generation is disabled
    return HttpResponse("PDF generation is currently disabled")