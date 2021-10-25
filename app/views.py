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

def cargar_barrios():

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

@login_required(login_url='/login/')
def index(request):

    lista_barrios = Barrio.objects.all()

    barrios = []

    for i in lista_barrios:
        barrios.append(
            {
                'id': i.id,
                'nombre': i.nombre,
                'cant_familias': i.cant_familias,
                'cant_paquetes': i.cant_paquetes,
                'localidad': i.localidad.all()[0].nombre,
                'provincia': i.localidad.all()[0].provincia.all()[0].nombre,
            }
        )

    print(barrios[0])

    return render(request, 'dashboard.html', {'barrios': barrios})

def localidades(request):

    localidades_obj = Localidad.objects.all()

    localidades = []

    for localidad in localidades_obj:

        cant_familias = localidad.cant_familias
        cant_paquetes = localidad.cant_paquetes

        localidades.append(
            {
                'nombre': localidad.nombre,
                'familias': cant_familias,
                'paquetes': cant_paquetes,
                'p4f': "{:.2f}".format(cant_paquetes / cant_familias),
                'provincia': localidad.provincia.all()[0].nombre
            }
        )

    return render(request, 'localidades.html', {'localidades': localidades})

def barrios_graves(request):

    if request.method == 'POST':

        cantidad = int(request.POST['cantidad'])

        lista_barrios = sorted(Barrio.objects.all(), key=lambda t: t.ratio)

        barrios = []

        for barrio in lista_barrios[0:cantidad]:
            barrios.append(
                {
                    'id': barrio.id,
                    'nombre': barrio.nombre,
                    'cant_familias': barrio.cant_familias,
                    'cant_paquetes': barrio.cant_paquetes,
                    'p4f': barrio.ratio,
                    'localidad': barrio.localidad.all()[0].nombre,
                    'provincia': barrio.localidad.all()[0].provincia.all()[0].nombre,
                }
        )

        return render(request, 'barrios_graves.html', {'barrios': barrios})
        
    else:
        return render(request, 'barrios_graves.html', {})

def barrio(request, id):

    barrio_obj = Barrio.objects.get(pk=id)

    barrio = {
        'id': barrio_obj.id,
        'nombre': barrio_obj.nombre,
        'cant_familias': barrio_obj.cant_familias,
        'cant_paquetes': barrio_obj.cant_paquetes,
        'localidad': barrio_obj.localidad.all()[0].nombre,
        'provincia': barrio_obj.localidad.all()[0].provincia.all()[0].nombre,
        'electricidad': barrio_obj.acceso_electricidad,
        'cloacas': barrio_obj.acceso_cloaca,
        'agua': barrio_obj.acceso_agua,
    }

    return render(request, 'barrio.html', {'barrio': barrio})

def agregar_paquetes(request, id):

    cantidad_paquetes = int(request.POST['cantidad_paquetes'])

    barrio_obj = Barrio.objects.get(pk=id)

    barrio_obj.incrementar_paquetes(cantidad_paquetes)

    barrio = {
        'id': barrio_obj.id,
        'nombre': barrio_obj.nombre,
        'cant_familias': barrio_obj.cant_familias,
        'cant_paquetes': barrio_obj.cant_paquetes,
        'localidad': barrio_obj.localidad.all()[0].nombre,
        'provincia': barrio_obj.localidad.all()[0].provincia.all()[0].nombre,
        'electricidad': barrio_obj.acceso_electricidad,
        'cloacas': barrio_obj.acceso_cloaca,
        'agua': barrio_obj.acceso_agua,
    }

    return render(request, 'barrio.html', {'barrio': barrio})

def buscar_prov_localidad(request):
    
    if request.method == 'POST':

        if request.POST.get('localidad') and request.POST.get('provincia'):
            
            provincia_exists = Provincia.objects.filter(
                Q(nombre=request.POST['provincia'])
            ).exists()       

            localidad_exists = Localidad.objects.filter(
                Q(nombre=request.POST['localidad']) &
                Q(provincia__nombre=request.POST['provincia'])
            ).exists()

            if provincia_exists:
                if localidad_exists:
                
                    localidad = Localidad.objects.get(
                        Q(nombre=request.POST['localidad']) &
                        Q(provincia__nombre=request.POST['provincia'])
                    )

                    lista_barrios = localidad.barrios.all()

                    barrios = []

                    for barrio in lista_barrios:
                        barrios.append({
                            'id': barrio.id,
                            'nombre': barrio.nombre,
                            'cant_familias': barrio.cant_familias,
                            'cant_paquetes': barrio.cant_paquetes,
                            'localidad': barrio.localidad.all()[0].nombre,
                            'provincia': barrio.localidad.all()[0].provincia.all()[0].nombre,
                        })
                
                    return render(request, '.html', {'barrios': barrios})
                else:
                    return render(request, '.html', {'error': 'Localidad no encontrada.'})
            else:
                return render(request, '.html', {'error': 'Provincia no encontrada.'}) 
        elif request.POST.get('provincia'):
    
            provincia_exists = Provincia.objects.filter(
                Q(nombre=request.POST['provincia'])
            ).exists()         

            if provincia_exists:
                lista_localidades = Localidad.objects.filter(
                    provincia__nombre=request.POST['provincia'] 
                ).all()

                localidades_barrios = {}

                for localidad in lista_localidades:
                    lista_barrios = localidad.barrios.all()
                    localidades_barrios[localidad.nombre] = []
                    for barrio in lista_barrios:
                        localidades_barrios[localidad.nombre].append({
                            'id': barrio.id,
                            'nombre': barrio.nombre,
                            'cant_familias': barrio.cant_familias,
                            'cant_paquetes': barrio.cant_paquetes,
                            'localidad': barrio.localidad.all()[0].nombre,
                            'provincia': barrio.localidad.all()[0].provincia.all()[0].nombre,
                        })
                        
                return render(request, '.html', {'localidad_barrios': localidades_barrios})
            else:
                return render(request, '.html', {'error': 'Provincia no encontrada.'})

        else:
            return render(request, '.html', {'error': 'No hay informacion para realizar la busqueda.'})

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