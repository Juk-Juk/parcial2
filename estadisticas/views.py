from django.shortcuts import render
from django.db.models import Count
from django.db.models.functions import TruncDate
from datetime import timedelta
from django.utils import timezone
from .models import Visita
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    # Get date range for last 30 days
    end_date = timezone.now()
    start_date = end_date - timedelta(days=29)
    
    # Daily visits using aggregate and annotate
    visitas_diarias = (
        Visita.objects
        .filter(fecha__gte=start_date)
        .annotate(dia=TruncDate('fecha'))
        .values('dia')
        .annotate(total=Count('id'))
        .order_by('dia')
    )
    
    # Prepare data for Chart.js
    labels_diarias = [v['dia'].strftime('%d/%m') for v in visitas_diarias]
    datos_diarias = [v['total'] for v in visitas_diarias]
    
    # Most visited pages using aggregate
    paginas_mas_visitadas = (
        Visita.objects
        .values('pagina')
        .annotate(total=Count('id'))
        .order_by('-total')[:10]
    )
    
    # Prepare data for Chart.js
    labels_paginas = [p['pagina'] for p in paginas_mas_visitadas]
    datos_paginas = [p['total'] for p in paginas_mas_visitadas]
    
    # Total statistics using aggregate
    total_visitas = Visita.objects.count()
    visitas_hoy = Visita.objects.filter(
        fecha__date=timezone.now().date()
    ).count()
    paginas_unicas = Visita.objects.values('pagina').distinct().count()
    
    context = {
        'labels_diarias': labels_diarias,
        'datos_diarias': datos_diarias,
        'labels_paginas': labels_paginas,
        'datos_paginas': datos_paginas,
        'total_visitas': total_visitas,
        'visitas_hoy': visitas_hoy,
        'paginas_unicas': paginas_unicas,
    }
    
    return render(request, 'dashboard.html', context)