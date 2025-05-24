from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.http import HttpResponse
from .models import ModelCV
from django.shortcuts import get_object_or_404
from django.template.loader import get_template

from weasyprint import HTML

class CVDetailView(DetailView):
    model = ModelCV
    template_name = 'main/template_detail.html'
    context_object_name = 'template_ctx'


class CVListView(ListView):
    model = ModelCV
    template_name = 'main/template_list.html'
    context_object_name = 'template_ctx'

def generate_pdf(request, pk):
    cv = get_object_or_404(ModelCV, id=pk)
    # Use the existing template
    template = get_template("main/template_detail.html")
    html_content = template.render(
        {"object": cv, "pdf_mode": True})  # Pass a flag for styling

    # Generate the PDF
    pdf_file = HTML(string=html_content).write_pdf()

    response = HttpResponse(pdf_file, content_type="application/pdf")
    response["Content-Disposition"] = \
        f'attachment; filename="{cv.firstname}_{cv.lastname}_CV.pdf"'

    return response
