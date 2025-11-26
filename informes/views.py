from django.views.generic import DetailView, ListView, CreateView
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.core.mail import EmailMessage
from django.conf import settings
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from io import BytesIO
from .models import Reporte, Alumno
from .forms import ReporteForm, AlumnoForm
from django.contrib.auth.decorators import login_required

class AlumnoListView(ListView):
    model = Alumno
    template_name = 'lista_alumnos.html'
    context_object_name = 'alumnos'

class AlumnoCreateView(CreateView):
    model = Alumno
    form_class = AlumnoForm
    template_name = 'crear_alumno.html'
    success_url = reverse_lazy('informes:lista_alumnos')

class ReporteListView(ListView):
    model = Reporte
    template_name = 'lista_reportes.html'
    context_object_name = 'reportes'

class ReporteCreateView(CreateView):
    model = Reporte
    form_class = ReporteForm
    template_name = 'crear_reporte.html'
    success_url = reverse_lazy('informes:lista_reportes')

class ReporteDetailView(DetailView):
    model = Reporte
    template_name = 'detalle_reporte.html'
    context_object_name = 'reporte'
    pk_url_kwarg = 'id'

@login_required
def generar_pdf(request, id):
    reporte = get_object_or_404(Reporte, id=id)
    alumno = reporte.alumno
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="reporte_{alumno.matricula}_{reporte.id}.pdf"'
    
    doc = SimpleDocTemplate(response, pagesize=letter)
    story = []
    
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#2c3e50'),
        alignment=TA_CENTER,
        spaceAfter=30,
    )
    
    subtitle_style = ParagraphStyle(
        'SubtitleStyle',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.HexColor('#34495e'),
        spaceAfter=20,
    )
    
    content_style = ParagraphStyle(
        'ContentStyle',
        parent=styles['Normal'],
        fontSize=12,
        alignment=TA_LEFT,
        spaceAfter=12,
    )
    
    # Title
    title = Paragraph(reporte.nombre, title_style)
    story.append(title)
    
    story.append(Spacer(1, 0.3*inch))
    
    # Student Information Table
    alumno_subtitle = Paragraph("Datos del Alumno", subtitle_style)
    story.append(alumno_subtitle)
    
    alumno_data = [
        ['Nombre:', alumno.nombre],
        ['Matrícula:', alumno.matricula],
        ['Carrera:', alumno.carrera],
        ['Email:', alumno.email],
        ['Fecha Ingreso:', alumno.fecha_ingreso.strftime('%d/%m/%Y')],
    ]
    
    alumno_table = Table(alumno_data, colWidths=[2*inch, 4*inch])
    alumno_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#ecf0f1')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ]))
    
    story.append(alumno_table)
    story.append(Spacer(1, 0.3*inch))
    
    # Report Information
    reporte_subtitle = Paragraph("Contenido del Reporte", subtitle_style)
    story.append(reporte_subtitle)
    
    fecha_texto = f"Fecha de creación: {reporte.fecha.strftime('%d/%m/%Y %H:%M')}"
    fecha = Paragraph(fecha_texto, content_style)
    story.append(fecha)
    story.append(Spacer(1, 0.2*inch))
    
    # Content
    contenido_parrafos = reporte.contenido.split('\n')
    for parrafo in contenido_parrafos:
        if parrafo.strip():
            p = Paragraph(parrafo, content_style)
            story.append(p)
    
    doc.build(story)
    
    return response

@login_required
def enviar_pdf_email(request, id):
    reporte = get_object_or_404(Reporte, id=id)
    alumno = reporte.alumno
    
    # Generate PDF in memory
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    story = []
    
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#2c3e50'),
        alignment=TA_CENTER,
        spaceAfter=30,
    )
    
    subtitle_style = ParagraphStyle(
        'SubtitleStyle',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.HexColor('#34495e'),
        spaceAfter=20,
    )
    
    content_style = ParagraphStyle(
        'ContentStyle',
        parent=styles['Normal'],
        fontSize=12,
        alignment=TA_LEFT,
        spaceAfter=12,
    )
    
    title = Paragraph(reporte.nombre, title_style)
    story.append(title)
    story.append(Spacer(1, 0.3*inch))
    
    alumno_subtitle = Paragraph("Datos del Alumno", subtitle_style)
    story.append(alumno_subtitle)
    
    alumno_data = [
        ['Nombre:', alumno.nombre],
        ['Matrícula:', alumno.matricula],
        ['Carrera:', alumno.carrera],
        ['Email:', alumno.email],
        ['Fecha Ingreso:', alumno.fecha_ingreso.strftime('%d/%m/%Y')],
    ]
    
    alumno_table = Table(alumno_data, colWidths=[2*inch, 4*inch])
    alumno_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#ecf0f1')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ]))
    
    story.append(alumno_table)
    story.append(Spacer(1, 0.3*inch))
    
    reporte_subtitle = Paragraph("Contenido del Reporte", subtitle_style)
    story.append(reporte_subtitle)
    
    fecha_texto = f"Fecha de creación: {reporte.fecha.strftime('%d/%m/%Y %H:%M')}"
    fecha = Paragraph(fecha_texto, content_style)
    story.append(fecha)
    story.append(Spacer(1, 0.2*inch))
    
    contenido_parrafos = reporte.contenido.split('\n')
    for parrafo in contenido_parrafos:
        if parrafo.strip():
            p = Paragraph(parrafo, content_style)
            story.append(p)
    
    doc.build(story)
    
    # Get PDF from buffer
    pdf_data = buffer.getvalue()
    buffer.close()
    
    # Send email
    email = EmailMessage(
        subject=f'Reporte: {reporte.nombre}',
        body=f'Hola {alumno.nombre},\n\nAdjunto encontrarás el reporte "{reporte.nombre}".\n\nSaludos cordiales.',
        from_email=settings.EMAIL_HOST_USER,
        to=[alumno.email],
    )
    
    email.attach(f'reporte_{alumno.matricula}_{reporte.id}.pdf', pdf_data, 'application/pdf')
    
    try:
        email.send()
        from django.contrib import messages
        messages.success(request, f'Reporte enviado exitosamente a {alumno.email}')
    except Exception as e:
        from django.contrib import messages
        messages.error(request, f'Error al enviar el reporte: {str(e)}')
    
    from django.shortcuts import redirect
    return redirect('informes:detalle_reporte', id=id)