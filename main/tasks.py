from celery import shared_task
from django.core.mail import EmailMessage
from django.conf import settings
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from io import BytesIO
import logging
from .models import ModelCV
from django.template.loader import get_template
logger = logging.getLogger(__name__)

@shared_task
def send_cv_pdf_email(cv_id, recipient_email):
    try:
        # Get CV from database
        cv = ModelCV.objects.get(id=cv_id)
        
        # Generate PDF
        pdf_buffer = generate_cv_pdf(cv)
        
        # Create email
        subject = f"CV - {cv.firstname} {cv.lastname}"
        message = f"""
Hello,

Please find attached the CV for {cv.firstname} {cv.lastname}.

Best regards,
Your CV System
        """
        
        email = EmailMessage(
            subject=subject,
            body=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[recipient_email],
        )
        
        # Attach PDF
        email.attach(
            f"CV_{cv.firstname}_{cv.lastname}.pdf",
            pdf_buffer.getvalue(),
            'application/pdf'
        )
        
        # Send email
        email.send()
        
        logger.info(f"CV PDF sent successfully to {recipient_email}")
        return {"status": "success", "message": f"Email sent to {recipient_email}"}
        
    except ModelCV.DoesNotExist:
        logger.error(f"CV with id {cv_id} not found")
        return {"status": "error", "message": "CV not found"}
    except Exception as e:
        logger.error(f"Error sending CV PDF email: {str(e)}")
        return {"status": "error", "message": str(e)}

def generate_cv_pdf(cv):
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    
    # Title
    p.setFont("Helvetica-Bold", 20)
    p.drawString(50, height - 50, f"CV - {cv.firstname} {cv.lastname}")
    
    # Basic info section
    y_position = height - 100
    p.setFont("Helvetica-Bold", 14)
    p.drawString(50, y_position, "Contact Information:")
    y_position -= 25
    
    p.setFont("Helvetica", 12)
    for key, value in cv.contacts.items():
        p.drawString(70, y_position, f"{key}: {value}")
        y_position -= 20
    
    # Biography section
    y_position -= 20
    p.setFont("Helvetica-Bold", 14)
    p.drawString(50, y_position, "Biography:")
    y_position -= 25
    
    p.setFont("Helvetica", 10)
    # Simple text wrapping for bio
    bio_lines = cv.bio.split('\n')
    for line in bio_lines:
        # Break long lines
        while len(line) > 80:
            p.drawString(70, y_position, line[:80])
            line = line[80:]
            y_position -= 12
            if y_position < 100:  # Check if we need a new page
                p.showPage()
                y_position = height - 50
        if line:
            p.drawString(70, y_position, line)
            y_position -= 12
    
    # Skills section
    y_position -= 20
    if y_position < 200:  # Check if we need a new page
        p.showPage()
        y_position = height - 50
        
    p.setFont("Helvetica-Bold", 14)
    p.drawString(50, y_position, "Skills:")
    y_position -= 25
    
    p.setFont("Helvetica", 10)
    for skill in cv.skills:
        p.drawString(70, y_position, f"• {skill}")
        y_position -= 15
        if y_position < 100:
            p.showPage()
            y_position = height - 50
    
    # Projects section
    y_position -= 20
    if y_position < 200:
        p.showPage()
        y_position = height - 50
        
    p.setFont("Helvetica-Bold", 14)
    p.drawString(50, y_position, "Projects:")
    y_position -= 25
    
    p.setFont("Helvetica", 10)
    for project in cv.projects:
        p.drawString(70, y_position, f"• {project}")
        y_position -= 15
        if y_position < 100:
            p.showPage()
            y_position = height - 50
    
    p.showPage()
    p.save()
    buffer.seek(0)
    return buffer