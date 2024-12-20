from django.shortcuts import render
from django.contrib.auth.models import User
from django.views.generic import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from apps.usuario.forms import RegistroForm
from rest_framework.views import APIView
from apps.usuario.serializers import UserSerializer
import json
from django.http import HttpResponse

class RegistroUsuario(CreateView):
    model = User
    template_name = "usuario/registrar_chef.html"
    form_class = RegistroForm
    success_url = reverse_lazy('registrar_chef')

class UserAPI(APIView):
    serializer = UserSerializer

    def get(self, request, format=None):
        lista = User.objects.all()
        response = self.serializer(lista, many=True)

        return HttpResponse(json.dumps(response.data), content_type='application/json')