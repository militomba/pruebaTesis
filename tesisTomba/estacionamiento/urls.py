from django.urls import path, include
from .views import *

app_name = 'estacionamiento'
urlpatterns = [
    path('', home, name='home'),
    path('funcion/', include([
    #path('asignar_lugar/', asignar_lugar_view, name='asignar_lugar'),
    path('detalleLugarAsignado/<str:cc>/', Funciones.detalleLugar, name='detalleLugar'),
    path('liberarLugar/<str:lugar>/', Funciones.liberarLugar, name='liberarLugar'),
    path('cc/<str:nombre>/', Funciones.centroComercial, name='cc'),
    ])),
    #centrosComerciales
    path('centroComercial/', CentrosComercialesViews.listCentroComercial, name='centroComercial'),
    path('centroComercial/<str:nombreCC>/', CentrosComercialesViews.detalle_centro, name='detalle_centro'),
    path('crearCentroComercial/', CentrosComercialesViews.crearCentroComercial, name='crearCentroComercial'),
    path('eliminarCentro/<str:nombre>/', CentrosComercialesViews.eliminarCentroComerial, name='eliminarCentro'),
    path('edicionCentro/<str:nombre>/', CentrosComercialesViews.edicionCentroComercial, name='edicionCentro'),
    #lugares
    path('lugares/<str:nombreCC>/', LugaresViews.listLugares, name='listLugares'),
    path('detalleLugar/<str:lugar>/<int:id_cc>/', LugaresViews.detalleLugar, name='detalleLugar'),
    path('crearLugar/<int:id_cc>', LugaresViews.crearLugar, name='crearLugar'),
    path('eliminarLugar/<str:lugar>', LugaresViews.eliminarLugar, name='eliminarLugar'),
    path('editarLugar/<str:nombreCC>/<str:lugar>', LugaresViews.editarLugar, name='editarLugar'),



]