from .models import Visita

class VisitaMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Save visit before processing the request
        Visita.objects.create(pagina=request.path)
        
        response = self.get_response(request)
        return response