from datetime import datetime
from pyexpat.errors import messages
from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from .models import Lugar, LugarOcupado, CentroComercialEspecifico
from django.urls import reverse
from django.core.files.base import ContentFile
import qrcode
from io import BytesIO
from rest_framework import viewsets, status
from rest_framework.response import Response


from django.core.files.uploadedfile import InMemoryUploadedFile
from django.http import HttpResponse
from django.db import IntegrityError
import jwt
from jwt.exceptions import InvalidTokenError
from datetime import datetime, timedelta
from django.core import serializers
from django.contrib.auth.decorators import login_required
import os
from tesisTomba.settings import SERVER_URL

class CentrosComercialesViews(viewsets.ViewSet):
    def listCentroComercial(request):
        ccListados = CentroComercialEspecifico.objects.all()
        return render(request, "gestionCentrosComerciales.html", {"cc": ccListados})
    
    def detalle_centro(request, nombreCC):
        centro = get_object_or_404(CentroComercialEspecifico, nombre =nombreCC)
        return render(request, 'detalle_centro.html', {'nombre': centro.nombre,'cantLugares': centro.cantidadLugares,'niveles':centro.niveles ,'imagen': centro.imagen.url})
        #return render(request, 'detalle_centro.html', {'cc': centro})

    def crearCentroComercial(request):
        if request.method == 'POST':
            nombre = request.POST.get('nombre')
            cantidad_lugares = int(request.POST.get('cantidadLugares'))
            niveles = int(request.POST.get('niveles'))
            # contenido = request.POST.get('contenido')
            imagen = request.FILES.get('imagen')

            try:
            # Crear el centro comercial
                centro_comercial = CentroComercialEspecifico(
                    nombre=nombre,
                    cantidadLugares=cantidad_lugares,
                    niveles=niveles,
                    # contenido=contenido
                )

                if imagen:
                    centro_comercial.imagen = imagen

                # Llamar a la función para generar el código QR y guardar la imagen
                centro_comercial.crear_centro_comercial()

                # Renderizar el template con el código QR generado
                return render(request, 'crearCentroComercial.html', {'qr_code': centro_comercial.imagen.url})
            except IntegrityError: 
                error_message = 'Ya existe un centro con el mismo nombre.'
                return render( request, 'crearCentroComercial.html', {'error': error_message})

        return render(request, 'crearCentroComercial.html')
    
    def eliminarCentroComerial(request, nombre):
        centroComercial=CentroComercialEspecifico.objects.get(nombre=nombre)
        if request.method == 'POST':
            centroComercial.delete()
            return redirect('estacionamiento:centroComercial') 
        return render(request, 'eliminarCentroComercial.html', {'centroComercial':centroComercial})

    def edicionCentroComercial(request, nombre):
        cc = CentroComercialEspecifico.objects.get(nombre=nombre)
        if request.method == 'POST':
            nombre = request.POST.get('nombre')
            cantidad_lugares = int(request.POST.get('cantidadLugares'))
            niveles = int(request.POST.get('niveles'))
            # contenido = request.POST.get('contenido')
            imagen = request.FILES.get('imagen')

            if (nombre != cc.nombre or
                cantidad_lugares != cc.cantidadLugares or
                niveles != cc.niveles or
                # contenido != cc.contenido or
                imagen is not None):
            # Al menos uno de los datos es diferente, se procede a realizar la actualización
            
                cc.nombre = nombre
                cc.cantidadLugares=cantidad_lugares
                cc.niveles = niveles
                # cc.contenido = contenido

                if imagen:
                    cc.imagen=imagen
                    
                cc.crear_centro_comercial()
                cc.save()

            return redirect('estacionamiento:detalle_centro', cc.nombre)

        return render(request, "edicionCentroCoemrcial.html", {'id':id,'nombre': cc.nombre,'cantLugares': cc.cantidadLugares,'niveles':cc.niveles ,'imagen': cc.imagen.url})

class LugaresViews(viewsets.ViewSet):
    def listLugares(request, nombreCC):
        centroComercial = get_object_or_404(CentroComercialEspecifico, nombre=nombreCC)

        lugar= Lugar.objects.filter(id_cc=centroComercial)
 
        return render(request, 'gestionLugares.html', {'lugar':lugar, 'centroComecial':centroComercial})            

    def detalleLugar(request, lugar, id_cc):
        detalleLugar= Lugar.objects.get(lugar=lugar, id_cc=id_cc)
        status = detalleLugar.status
        centroComercial = detalleLugar.id_cc.nombre
        cantidadLugares = detalleLugar.id_cc.cantidadLugares
        qr = detalleLugar.codigo_qr        
        if status == True:
            status="ACTIVO"
        else:
            status='INACTIVO'
        
        qr_vacio = False
        if not detalleLugar.codigo_qr:
            qr_vacio = True
        return render(request, 'detalleLugar.html', {'lugar': detalleLugar.lugar, 'status':status, 'nivel':detalleLugar.nivel, 'centroComercial':centroComercial, 'qr':qr, 'qr_vacio': qr_vacio, 'id_cc':detalleLugar.id_cc})
    
    def eliminarLugar(request, lugar):
        lugar = Lugar.objects.get(lugar=lugar)
        cc = lugar.id_cc.nombre
        if request.method == 'POST':
            lugar.delete()
            return redirect('estacionamiento:listLugares', cc) 
        return render(request, 'eliminarLugar.html', {'lugar':lugar})
                
    def crearLugar(request, id_cc):
        centroComercial=CentroComercialEspecifico.objects.get(id=id_cc)
        if request.method == 'POST':
            lugar = request.POST.get('lugar')
            nivel = int(request.POST.get('nivel'))
            status = request.POST.get('status')
            codigo_qr = request.FILES.get('codigo_qr')
            id_cc = request.POST.get('id_cc')

            lugar_existente = Lugar.objects.filter(lugar=lugar, id_cc=centroComercial.id)

            if lugar_existente.exists():
                error = "Ya existe un lugar con este nombre en el centro comercial."
                return render(request, 'crearLugar.html', {'cc': centroComercial, 'error': error})
        
            lugarNuevo = Lugar(lugar= lugar,
                            nivel=nivel,
                            status=status,
                            id_cc=centroComercial, 
                            codigo_qr=codigo_qr)
            
            lugarNuevo.save()
            return redirect('estacionamiento:listLugares', centroComercial.nombre )
            #return render(request, 'crearLugar.html', {'lugar':lugarNuevo, 'cc':centroComercial})
            
            
        return render(request, 'crearLugar.html', {'cc':centroComercial})
    
    def editarLugar(request, nombreCC, lugar):
        l= Lugar.objects.get(lugar=lugar)
        cc =CentroComercialEspecifico.objects.get(nombre=nombreCC)
        if request.method == 'POST':
            lugar = request.POST.get('lugar')
            nivel = int(request.POST.get('nivel'))
            status = request.POST.get('status')
            id_cc = request.POST.get('id_cc')

            if(lugar != l.lugar or
               nivel != l.nivel or
               status != l.status):
                
                l.lugar=lugar
                l.nivel=nivel
                l.status=status
                l.id_cc=cc

                l.save()

            return redirect('estacionamiento:detalleLugar', lugar=l.lugar, id_cc=cc.id)
        
        return render(request, 'editarLugar.html', {'lugar':l, 'cc':cc})
                



class Funciones(viewsets.ViewSet):
    def asignarLugar(cc):
        
        centroComercial=CentroComercialEspecifico.objects.get(nombre=cc)

        lugarAsignado = Lugar.objects.filter(status=True, id_cc=centroComercial.id).first()
  
        
        if lugarAsignado is None:
            #hacer funcion para verificar si hay alguno expirado y asignar ese
            return None
        
        
        lugarAsignado.status = False
        lugarAsignado.save()

        #agrego un lugar a la tabla LugarOcupado
        lugarOcupado = LugarOcupado.objects.create(lugar=lugarAsignado,   
                                                fecha = datetime.now().date(),
                                                hora_entrada = datetime.now().time()) 
                                                
        lugarOcupado.save()
        
        centroComercial = lugarAsignado.id_cc.nombre
        
        
        
        archivo_jwt={
            'lugar':lugarOcupado.lugar.lugar,
            'exp': datetime.utcnow() + timedelta(hours=24)
        }

        token = jwt.encode(archivo_jwt, 'Alaska.1234', algorithm='HS256')
        

        #generar codigo QR
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data('http://'+SERVER_URL+'/funcion/liberarLugar/'+str(lugarAsignado.lugar)+'/?token=' + token)
        qr.make(fit=True)
        img = qr.make_image(fill='black', back_color='white')

        #guardar qr
        buffer = BytesIO()
        img.save(buffer, 'PNG')
        buffer.seek(0)
        qr_file = InMemoryUploadedFile(buffer, None, lugarAsignado.lugar+centroComercial+'.png', 'img/png', buffer.getbuffer().nbytes, None)
        # lugarAsignado.codigo_qr.save(f'{lugarAsignado.lugar}.png',ContentFile(buffer.getvalue()),save=False)
        lugarAsignado.codigo_qr.save(lugarAsignado.lugar+centroComercial+'.png', qr_file, save=True)
        lugarAsignado.save()

        imagen = lugarAsignado.codigo_qr.url

        info={
            'lugar': lugarOcupado.lugar,
            'nivel':lugarAsignado.nivel,
            'fecha':lugarOcupado.fecha,
            'horario':lugarOcupado.hora_entrada,
            'centroComercial': centroComercial,
            'imagen': imagen
        }
        
        
        return info



    @login_required
    def liberarLugar(request, lugar):
        user=request.user
       
        token = request.GET.get('token')

        try:
            #payload = jwt.decode(token, 'user.data.token', algorithms=['HS256'])
            payload = jwt.decode(token, 'Alaska.1234', algorithms=['HS256'])
            lugarAsignado = Lugar.objects.filter(lugar=lugar).first()
            
            if lugarAsignado is None:
                return HttpResponse("El lugar no fue encontrado")
            centroComercial = lugarAsignado.id_cc.nombre
            lugarAsignado.status = True
            lugarAsignado.save()
            
            lugarOcupado = LugarOcupado.objects.filter(lugar=lugarAsignado).last()
            lugarOcupado.delete()
            lugarAsignado.codigo_qr.delete()
            context ={
                'lugar':lugarAsignado.lugar,
                'centroComercial': lugarAsignado.id_cc.nombre
            }
            # print(f"Lugar: {lugarAsignado.lugar} liberado del centro comercial: {centroComercial}")
            return render(request, 'liberarLugar.html', context)
            #return HttpResponse('Lugar '+str(lugarAsignado.lugar)+' liberado exitosamente')
        except InvalidTokenError:
            return HttpResponse("Token inválido")
        


    def detalleLugar(request, cc):
        token = request.GET.get('token')
        try:
            payload = jwt.decode(token, '1234', algorithms=['HS256'])
            cc = CentroComercialEspecifico.objects.get(nombre=cc)
            
            infoLugar = Funciones.asignarLugar(cc)
            
            if infoLugar:
                lugar = infoLugar['lugar']
                nivel =infoLugar['nivel']
                imagen = infoLugar['imagen']
                fecha=infoLugar['fecha']
                hora = infoLugar['horario']
                centroComercial = infoLugar['centroComercial']
                
                
                context={
                    'lugar': lugar,
                    'nivel':nivel,
                    'fecha':fecha,
                    'horario':hora,
                    'imagen': imagen,
                    'centroComercial': centroComercial
                }
                

                return render(request, 'detalleLugarAsignado.html', context)
            else:
                archivo_jwt={
                'cc':cc.nombre,
                'exp': datetime.utcnow() + timedelta(hours=24)
                }

                token = jwt.encode(archivo_jwt, 'Alaska.1234', algorithm='HS256')
                

                #generar codigo QR
                qr = qrcode.QRCode(version=1, box_size=10, border=5)
                qr.add_data('abrirBarrera/?token=' + token)
                qr.make(fit=True)
                img = qr.make_image(fill='black', back_color='white')
                qr_filename = cc.nombre + '.png'
                qr_path = os.path.join(settings.MEDIA_ROOT, qr_filename)
                img.save(qr_path)

                # Obtener la URL del archivo QR
                qr_url = os.path.join(settings.MEDIA_URL, qr_filename)
                
                return render(request, 'sin_lugares.html', {'cc':cc.nombre, 'imagen':qr_url})
            
            
        except InvalidTokenError:
            return HttpResponse("Token inválido")

    def centroComercial(request, nombre):
        centro_comercial = CentroComercialEspecifico.objects.get(nombre__iexact=nombre)
        return render(request, 'detalle_centro_comercial.html', {'nombre': centro_comercial.nombre, 'imagen': centro_comercial.imagen.url})