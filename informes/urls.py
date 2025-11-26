from django.urls import path
from . import views

app_name = 'informes'

urlpatterns = [
    path('', views.ReporteListView.as_view(), name='lista_reportes'),
    path('alumnos/', views.AlumnoListView.as_view(), name='lista_alumnos'),
    path('reporte/crear/', views.ReporteCreateView.as_view(), name='crear_reporte'),
    path('reporte/<int:id>/', views.ReporteDetailView.as_view(), name='detalle_reporte'),
    path('reporte/<int:id>/pdf/', views.generar_pdf, name='generar_pdf'),
    path('reporte/<int:id>/enviar/', views.enviar_pdf_email, name='enviar_pdf'),
]