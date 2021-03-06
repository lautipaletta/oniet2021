from django.db import models

# Create your models here.

class Provincia(models.Model):
    nombre = models.CharField('Nombre', max_length=50, null=False, blank=False)
    localidades = models.ManyToManyField('Localidad', null=False, blank=False, related_name='provincia')

    def __str__(self):
        return self.nombre

class Localidad(models.Model):
    nombre = models.CharField('Nombre', max_length=50, null=False, blank=False)
    barrios = models.ManyToManyField('Barrio', null=False, blank=False, related_name='localidad')

    @property
    def cant_barrios(self):
        return len(self.barrios.all())

    @property
    def cant_paquetes(self):
        cant = 0
        for barrio in self.barrios.all():
            cant += barrio.cant_paquetes
        return cant

    @property
    def cant_familias(self):
        cant = 0
        for barrio in self.barrios.all():
            cant += barrio.cant_familias
        return cant

    def __str__(self):
        return self.nombre

class Barrio(models.Model):
    nombre = models.CharField('Nombre', max_length=50, null=False, blank=False)
    cant_familias = models.IntegerField('Cantidad Familias', null=False, blank=False, default=0)
    cant_paquetes = models.IntegerField('Cantidad Paquetes', null=False, blank=False, default=0)
    acceso_electricidad = models.CharField('Acceso Luz', max_length=50, null=False, blank=False)
    acceso_cloaca = models.CharField('Acceso Cloacas', max_length=50, null=False, blank=False)
    acceso_agua = models.CharField('Acceso Agua', max_length=50, null=False, blank=False)

    def incrementar_paquetes(self, cantidad):
        self.cant_paquetes += cantidad
        self.save()

    @property
    def ratio(self):    
        return "{:.2f}".format(self.cant_paquetes / self.cant_familias)

    def __str__(self):
        return self.nombre