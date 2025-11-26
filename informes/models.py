from django.db import models

class Alumno(models.Model):
    nombre = models.CharField(max_length=200)
    email = models.EmailField()
    carrera = models.CharField(max_length=200)
    matricula = models.CharField(max_length=50, unique=True)
    fecha_ingreso = models.DateField()
    
    class Meta:
        ordering = ['nombre']
    
    def __str__(self):
        return f"{self.nombre} - {self.matricula}"

class Reporte(models.Model):
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE, related_name='reportes', default=1)
    nombre = models.CharField(max_length=200)
    contenido = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-fecha']
    
    def __str__(self):
        return self.nombre