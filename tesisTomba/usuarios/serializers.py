from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import *
class TipoUsuarioSerializer(serializers.ModelSerializer):
    class Meta():
        model = TipoUsuarios
        fields = '__all__'

class TipoUsuarioCreateSerializer(serializers.ModelSerializer):
    class Meta():
        model = TipoUsuarios
        fields = ('tipo_usuario',)

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta():
        model = DatosUsuarios
        fields = '__all__'

class UsuarioCreateSerializer(serializers.ModelSerializer):
    class Meta():
        model = DatosUsuarios
        fields = ('usuario', 'nombre','apellido', 'email', 'tipo',)

class UsuarioUpdateSerializer(serializers.ModelSerializer):
    class Meta():
        model = DatosUsuarios
        fields = ('nombre','apellido', 'email', 'tipo',)