from django.db import models

class Visita(models.Model):
    pagina = models.CharField(max_length=500)
    fecha = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-fecha']
    
    def __str__(self):
        return f"{self.pagina} - {self.fecha}"