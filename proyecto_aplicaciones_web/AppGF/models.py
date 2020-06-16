from django.db import models
from datetime import datetime
from django.utils import formats
from django.utils import timezone

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from oscar.apps.catalogue.models import Product

# Create your models here.

from django.db import models
  
    
class Usuario(models.Model):	
	
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key= True)
    correo = models.EmailField(max_length=200)
    provincia = models.CharField(max_length=200)
    localidad = models.CharField(max_length=200)
    experiencia_como_pescador = models.TextField()
    foto_usuario = models.FileField(upload_to='perfil_usuarios',blank=True)
    
    
    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def update_user_usuario(sender, instance, created, **kwargs):
    if created:
        Usuario.objects.create(user=instance)
    instance.usuario.save()        
      

class ZonaPesca(models.Model):
    zona_cercana = models.CharField(max_length=200)
    coordenadas_zona = models.CharField(max_length=70,blank=True)
    
    
    def __str__(self):
        return self.zona_cercana      
    
class Pescado(models.Model):
    nombre_comun_pescado = models.CharField(max_length=200)
    nombre_cientifico = models.CharField(max_length=200,blank=True)
    foto_pescado = models.ImageField(upload_to='pescados',blank=True)
    #peso_minimo =
    #peso_ maximo =
    descripcion_pescado = models.TextField()

    class Meta:
        ordering = ['nombre_comun_pescado']

    def __str__(self):
        return str(self.nombre_comun_pescado)

        
class MaterialSeñuelo(models.Model):
    material_señuelo = models.CharField(max_length=200)
    
    def __str__(self):
        return self.material_señuelo        
    
class Señuelo(models.Model):
    nombre_señuelo = models.CharField(max_length=200)
    peso_señuelo = models.CharField(max_length=200,blank=True)
    modelo_señuelo = models.CharField(max_length=200,blank=True)
    material_señuelo = models.ForeignKey(MaterialSeñuelo, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.nombre_señuelo
         

class Marea(models.Model):
	estado = models.CharField(max_length=200)
	
	def __str__(self):
		return self.estado
        
class Captura(models.Model):
	fecha_captura = models.DateField("Fecha DD/MM/YYYY")		
	pescado = models.ForeignKey(Pescado, on_delete=models.CASCADE)
	cantpes = models.IntegerField(default=1)
	señuelo = models.ForeignKey('catalogue.Product', on_delete=models.CASCADE)
	carrete = models.ForeignKey('catalogue.Product', on_delete=models.CASCADE, related_name='carrete')
	caña = models.ForeignKey('catalogue.Product', on_delete=models.CASCADE, related_name='caña')
	usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
	zona = models.ForeignKey(ZonaPesca, on_delete=models.CASCADE)
	marea = models.ForeignKey(Marea, on_delete=models.CASCADE)
	foto_captura = models.ImageField(upload_to='capturas',blank=True)
	
	class Meta:
		ordering = ['-fecha_captura', 'pescado']
	
	def __str__(self):
		return str(self.fecha_captura)
