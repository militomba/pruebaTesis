from django.urls import path, include
from .views import *
app_name = 'usuarios'
urlpatterns = [
        path('', Usuarios.home, name='home'),
        path('login/', Usuarios.user_login, name='login'),
        path('register/', Usuarios.register, name='register'),
        path('administrador/', Usuarios.administrador, name='administrador'),
        path('listadoUsuario/', Usuarios.listUsuario, name='usuario'),
        path('detalleusuario/<int:usuarioID>', Usuarios.detalleUsuario, name='detalleUsuario'),
        path('agregarCentro/<int:usuarioID>', Usuarios.agregarCentroComercial, name='agregarCentro'),
        path('scanner/', Usuarios.scanner, name='scanner'),
        path('logout/', Usuarios.user_logout, name='logout')

    
]