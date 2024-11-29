from django.db import models
from django.conf import settings
from estacionamiento.models import *
from django.contrib.auth.hashers import make_password


class TipoUsuarios(models.Model):
    
    ADMINISTRADOR = 'Administrador'
    CENTRO_COMERCIAL = 'Centro Comercial'
    SCANNER_QR = 'Scanner QR'

    TIPO_USUARIO_CHOICES = [
        (ADMINISTRADOR, 'Administrador'),
        (CENTRO_COMERCIAL, 'Centro Comercial'),
        (SCANNER_QR, 'Scanner QR')
    ]

    tipo_usuario = models.CharField(max_length=101, choices=TIPO_USUARIO_CHOICES)

    def __str__(self):
        return self.tipo_usuario

class DatosUsuarios(models.Model):
    usuario = models.CharField(max_length=100)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=128, default=True)
    tipoUsuario= models.ForeignKey(TipoUsuarios, on_delete=models.CASCADE, null=False, default=True)
    centroComercial=models.ForeignKey(CentroComercialEspecifico, on_delete=models.CASCADE, null=True, blank=True, default=True)
    
    def __str__(self):
        return self.usuario
    
class Scanner(DatosUsuarios):
    token = models.CharField(max_length=500)



    
   