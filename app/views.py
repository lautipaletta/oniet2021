from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
from django.conf import settings
from django.db.models import Q
from .models import Provincia, Localidad, Barrio
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
import json

# Create your views here.

@login_required(login_url='/login/')
def index(request):

    # for barrio in Barrio.objects.all():
    #     barrio.delete()

    # for provincia in Provincia.objects.all():
    #     provincia.delete()

    # for localidad in Localidad.objects.all():
    #     localidad.delete()

    file = open(settings.BASE_DIR / 'dataset.json', 'r')

    dataset = json.load(file)

    for objeto in dataset['features']:

        propiedades = objeto['properties']

        provincia = propiedades['Provincia']
        localidad = propiedades['Localidad']
        barrio = propiedades['Barrio']

        barrio_agua = propiedades['Agua']
        barrio_electricidad = propiedades['Electricidad']
        barrio_cloaca = propiedades['Cloaca']
        barrio_familias = propiedades['Familias estimadas']

        # print(f"{provincia} - {localidad} - {barrio} - Agua: {barrio_agua} - Electricidad: {barrio_electricidad} - Cloaca: {barrio_cloaca} - Familias: {barrio_familias}")

        provincia_exists = Provincia.objects.filter(nombre=provincia).exists()

        localidad_exists = Localidad.objects.filter(
            Q(nombre=localidad)
            # Q(provincia__nombre=provincia)
        ).exists()

        barrio_exists = Barrio.objects.filter(
            Q(nombre=barrio)
            # Q(localidad__nombre = localidad) &
            # Q(localidad__provincia__nombre = provincia)
        ).exists()

        if not provincia_exists:
            Provincia.objects.create(nombre=provincia)

        if not localidad_exists:
            Localidad.objects.create(nombre=localidad)

        if not barrio_exists:
            Barrio.objects.create(
                nombre=barrio,
                cant_familias = barrio_familias,
                acceso_electricidad = barrio_electricidad,
                acceso_cloaca = barrio_cloaca,
                acceso_agua = barrio_agua
            )

        provincia_obj = Provincia.objects.get(nombre=provincia)
        localidad_obj = Localidad.objects.get(nombre=localidad)
        barrio_obj = Barrio.objects.get(nombre=barrio)

        if not localidad_obj in provincia_obj.localidades.all():
            provincia_obj.localidades.add(localidad_obj)

        if not barrio_obj in localidad_obj.barrios.all():
            localidad_obj.barrios.add(barrio_obj)

        # try:
        #     localidad_obj = Localidad.objects.get(
        #         Q(nombre=localidad) & Q(provincia__nombre = provincia)
        #     )
        # except MultipleObjectsReturned:
        #     pass
        # except ObjectDoesNotExist:
        #     Provincia.objects.get(nombre=provincia).localidades.add(Localidad.objects.get(nombre=localidad))

        # try:
        #     barrio_obj = Barrio.objects.get(
        #         Q(nombre=barrio) & Q(localidad__nombre = localidad) & Q(localidad__provincia__nombre=provincia)
        #     )
        # except MultipleObjectsReturned:
        #     pass
        # except ObjectDoesNotExist:
        #     Localidad.objects.get(nombre=localidad).barrios.add(Barrio.objects.get(nombre=barrio))

    return HttpResponse('Done')

def agregar_paquetes(request, id):

    cantidad_paquetes = int(request.POST['cantidad_paquetes'])

    barrio = Barrio.objects.get(pk=id)

    barrio.incrementar_paquetes(cantidad_paquetes)

    return render(request, 'barrio.html', {})



def login(request):
    
    if request.method == 'POST':
        
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user:

            auth_login(request, user)

            return redirect('index')

        else:

            return render(request, 'login.html', {'error_message': 'El email o el usuario ingresados son incorrectos.'})

    else:
        return render(request, 'login.html', {})

def logout(request):
    auth_logout(request)
    return redirect('login')