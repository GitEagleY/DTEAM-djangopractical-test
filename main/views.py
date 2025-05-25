from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.template.loader import get_template
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
import json

from weasyprint import HTML

from .models import ModelCV, RequestLog
from .tasks import send_cv_pdf_email


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

    # Generate PDF
    pdf_file = HTML(string=html_content).write_pdf()
    response = HttpResponse(pdf_file, content_type="application/pdf")
    response["Content-Disposition"] = \
        f'attachment; filename="{cv.firstname}_{cv.lastname}_CV.pdf"'

    return response


@require_http_methods(["POST"])
def send_cv_email(request, pk):
    """
    Handle AJAX request to send CV PDF via email
    """
    try:
        # Get CV
        cv = get_object_or_404(ModelCV, id=pk)
        
        # Parse JSON data
        data = json.loads(request.body)
        recipient_email = data.get('email', '').strip()
        
        # Validate email
        if not recipient_email:
            return JsonResponse({
                'status': 'error',
                'message': 'Email address is required'
            }, status=400)
            
        try:
            validate_email(recipient_email)
        except ValidationError:
            return JsonResponse({
                'status': 'error',
                'message': 'Please enter a valid email address'
            }, status=400)
        
        # Queue the email task
        task = send_cv_pdf_email.delay(cv.id, recipient_email)
        
        return JsonResponse({
            'status': 'success',
            'message': f'CV is being sent to {recipient_email}',
            'task_id': task.id
        })
        
    except json.JSONDecodeError:
        return JsonResponse({
            'status': 'error',
            'message': 'Invalid request data'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': f'An error occurred: {str(e)}'
        }, status=500)