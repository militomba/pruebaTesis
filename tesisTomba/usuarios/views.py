from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import viewsets
from .models import *
from django.contrib.auth.models import Group, Permission
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, get_object_or_404, redirect
from estacionamiento.models import *
from django.contrib.auth.models import User



class Usuarios(viewsets.ViewSet):
    def home(request):
        context = {
            'author': 'Milagros Tomba',
            'faculty': 'Facultad de Ingeniería',
            'university': 'Universidad de Mendoza',
            'project_date': "2024",
            'description': 'Proyecto de tesis para la automatización de los estacionamientos de los centros comerciales.',
        }
        return render(request, 'home.html', context)
    def register(request):
        if request.method == 'POST':
            username = request.POST['usuario']
            password = request.POST['password']
            email = request.POST['email']
            nombre = request.POST['nombre']
            apellido = request.POST['apellido']
            tipoUsuario = request.POST['tipo_usuario']
            # Crear un nuevo usuario en la base de datos
            

            user = User.objects.create_user(username=username, password=password, email=email)

            tipo_usuario = TipoUsuarios.objects.get(id=tipoUsuario)
            
            if tipoUsuario=='3':
                datos_usuario=Scanner(usuario=username, nombre=nombre, apellido=apellido, email=email, password=password, tipoUsuario=tipo_usuario, token='Alaska.1234', centroComercial=None)
            else:
                datos_usuario = DatosUsuarios(usuario=username, nombre=nombre, apellido=apellido, email=email, password=password, tipoUsuario=tipo_usuario, centroComercial=None)
            datos_usuario.save()
            return redirect('usuarios:login')
        
        tipoUsuarios = TipoUsuarios.objects.all()
        return render(request, 'register.html', {'tipoUsuario': tipoUsuarios})

    def user_login(request):
        if request.method == 'POST':
            username = request.POST['usuario']
            password = request.POST['password']

            if not username or not password:
                return render(request, 'login.html', {'error': 'Por favor, complete ambos campos.'})
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                try:
                   datos_usuario = DatosUsuarios.objects.get(usuario=user)
                except:
                    return render(request, 'login.html', {'error': 'Datos de usuario no encontrados.'})
                
                tipo_usuario = datos_usuario.tipoUsuario.tipo_usuario
                if tipo_usuario == 'Administrador':
                    return redirect('usuarios:administrador')  # Redirigir a la página del administrador
                elif tipo_usuario == 'Centro Comercial':
                    return redirect('estacionamiento:listLugares', datos_usuario.centroComercial.nombre)  # Redirigir a la página del centro comercial
                elif tipo_usuario == 'Scanner QR':
                    return redirect('usuarios:scanner')
                    # return redirect('usuarios:scanner', datos_usuario.id)  # Redirigir a la página del scanner QR # Redirigir a la página de inicio
            else:
                return render(request, 'login.html', {'error': 'Usuario o contraseña incorrectos'})
        return render(request, 'login.html')




    # def user_login(request):
    #     if request.method == 'POST':
    #         username = request.POST['usuario']
    #         password = request.POST['password']
    #         # Autenticar al usuario
    #         user = authenticate(request, username=username, password=password)
    #         if user is not None:
    #         # Iniciar sesión
    #             login(request, user)
    #             datos_usuario = DatosUsuarios.objects.get(usuario=username)
    #             tipo_usuario = datos_usuario.tipoUsuario.tipo_usuario
    #             if tipo_usuario == 'Administrador':
    #                 return redirect('usuarios:administrador')  # Redirigir a la página del administrador
    #             elif tipo_usuario == 'Centro Comercial':
    #                 return redirect('estacionamiento:listLugares', datos_usuario.centroComercial.nombre)  # Redirigir a la página del centro comercial
    #             elif tipo_usuario == 'Scanner QR':
    #                 return redirect('usuarios:scanner', datos_usuario.id)  # Redirigir a la página del scanner QR # Redirigir a la página de inicio
    #         else:
    #             # Usuario no válido
    #             return render(request, 'login.html', {'error': 'Usuario o contraseña incorrectos'})
    #     return render(request, 'login.html')

    def user_logout(request):
        logout(request)
        return redirect('usuarios:login')
    

    #ADMINISTRADOR
    def administrador(request):
        return render(request, 'admin.html')
    
    def listUsuario(request):
        listadoUsuarios = DatosUsuarios.objects.exclude(tipoUsuario__tipo_usuario='Administrador')
        
        return render(request, 'usuario.html', {'listadoUsuario':listadoUsuarios})
    # def listUsuario(request):
    #     user=request.user
    #     if request.user.is_authenticated:
    #         # usuarios=DatosUsuarios.objects.all()
    #         usuarios=DatosUsuarios.objects.get(usuario=user)
    #         nombre = usuarios.usuario
    #         tipoUsuarios= usuarios.tipoUsuario.tipo_usuario
    #         if tipoUsuarios == 'Administrador':
    #             usuario= DatosUsuarios.objects.exclude(usuario=nombre)
                
    #         return render(request, 'usuario.html', {'usuario':usuario})
    #     return redirect('usuarios:login')
    
    def detalleUsuario(request, usuarioID):
        usuario = get_object_or_404(DatosUsuarios, id=usuarioID)
        cc_vacio=False
        if not usuario.centroComercial:
            cc_vacio=True
        return render (request, 'detalleUsuario.html', {'usuario':usuario, 'cc_vacio':cc_vacio})

    def agregarCentroComercial(request, usuarioID):
        cc = CentroComercialEspecifico.objects.all()
        usuario = get_object_or_404(DatosUsuarios, id=usuarioID)
        
        if request.method == 'POST':
            centroComercial = request.POST.get('centroComercial')
            centro = get_object_or_404(CentroComercialEspecifico, id=centroComercial)
            
            usuario.centroComercial = centro
            usuario.save()
            return redirect('usuarios:detalleUsuario', usuarioID)
        
        return render(request, 'agregarCentroComercial.html', {'cc': cc, 'usuario': usuario})
    
    # def scanner(request, usuarioID):
    #     usuario = DatosUsuarios.objects.get(id=usuarioID)
    #     user=usuario.usuario
    #     id_user = usuario.id
    #     print({user})
    #     print({usuario.id})
    #     return render(request, 'scanner.html', {'usuario':user})

    def scanner(request):
        return render(request, 'scanner.html')

    #USUARIOS CENTROS COMERCIALES
        
    
    


