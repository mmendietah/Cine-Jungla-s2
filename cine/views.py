from django.shortcuts import render, redirect
from .froms import addProd, regFrom
from .models import Registrado, Multiplex, Silla, Pelicula
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as do_login
from django.contrib.auth import logout as do_logout
from django.contrib.auth.models import Group
from django.core.mail import send_mail
from django.conf import settings

# from passlib.hash import pbkdf2_sha256

productos = {'combo 1': 5,
             'Queso': 2,
             'Gomita': 4,
             'Tocineta': 0,
             }
lista = {}

def confiteria(request):
   return render(request, "confiteria.html")

def peliculas(request):
   multiplex = Multiplex.objects.all()
   peliculas = Pelicula.objects.all()
   context ={
      "multi": multiplex,
      "pelis": peliculas
   }
   return render(request, "peliculas.html", context)

def recibo(request):
   return render(request, "recibo.html")

def enviarCorreo(request):
   form = regFrom(request.POST or None)

   # print(dor(form))
   if form.is_valid():
      formData = form.cleaned_data
      email = formData.get("email")
      nombre = formData.get("nombre")
      mensaje2 = formData.get("mensaje")
      mensaje = mensaje2 + "Hola "+nombre\
                +"\n Tambien te queremos invitar a llenar esta encuesta de satisfacción:\n https://forms.gle/JvDjdpKkBU5oqd1d7"
      asunto = "Cine Jungla"
      emailFrom = settings.EMAIL_HOST_USER
      emailTO = [email, "rmacias@unbosque.edu.co"]

      send_mail(asunto,
                mensaje,
                emailFrom,
                emailTO,
                fail_silently=False
                )

      print(nombre, "\t", email, "\t", mensaje, "\t")
   context = {

      "el_form": form,
   }
   return render(request, "correo.html", context)

def asientos(request):
   sillas = Silla.objects.all()
   Silla.objects.filter(estado_silla=2).update(estado_silla=0)
   if request.method == "POST":
      pelicula = request.POST['p']
      multiplex = request.POST['m']
      context = {
         "sillas": sillas,
         "pelicula": pelicula,
         "multiplex": multiplex
      }
   else:
      context = {
         "sillas": sillas
      }
   return render(request, "asientos.html", context)

def comprar(request):
   if request.method == "POST":
      pag = request.POST['pag']
      pelicula = request.POST['p']
      multiplex = request.POST['m']
      silla1 = request.POST.getlist('id')
      lista = []
      for tipo in silla1:
         lista.append(Silla.objects.filter(id=tipo))
      print(lista)
      if pag == 'C':
         context = {
            "sillas": silla1,
            "pelicula": pelicula,
            "multiplex": multiplex
         }
         for silla in silla1:
            Silla.objects.filter(id = silla).update(estado_silla = 1)
         return render(request, "recibo.html", context)
      if pag == 'R':
         for silla in silla1:
            Silla.objects.filter(id = silla).update(estado_silla = 2)
         silla2 = Silla.objects.all()
         context = {
            "sillas": silla2,
         }
   return render(request, "asientos.html", context)

def inicio(request):
   if request.user.is_authenticated:
      return render(request, "inicio.html")
   else:
      return redirect('../')

def login(request):
   if request.method == "POST":

      username = request.POST['nombre']
      password = request.POST['pass']
      user = authenticate(username=username, password=password)
      # hash = pbkdf2_sha256.hash("123456")
      # print(pbkdf2_sha256.verify("password", hash))
      # print(hash)
      if user is not None:
         do_login(request, user)
         grupo = Group.objects.get(user=user)
         if grupo.id == 2:
            return render(request, "inicio.html")
         else:
            return render(request, "confiteria.html")
   return render(request, "registration/login.html")

# def login(request):
#    return render(request, "inicio.html")

def logout(request):
   do_logout(request)
   return redirect('login')


def img_multiplex(request):
   imgs = Multiplex.objects.all()
   for i in imgs:
      print(imgs.nombre)
   return render(request, "inicio.html", {'imagenes': imgs})

def selecProducto(request):

   form = addProd(request.POST or None)
   submit = request.POST

   if (productos['combo 1'] == 0):
      enable = False
   else:
      enable = True
   if (productos['Queso'] == 0):
      enable1 = False
   else:
      enable1 = True

   if (productos['Gomita'] == 0):
      enable2 = False
   else:
      enable2 = True

   if (productos['Tocineta'] == 0):
      enable3 = False
   else:
      enable3 = True

   if form.is_valid():

      formData = form.cleaned_data
      nombre = formData.get('nombre')

      if (submit.get('combo1')):
         print("Nombre ", nombre)
         print("Selecciono el Combo 1 ")

         var = nombre
         enable = realizarmetodo(var)
         print(productos)
         print(lista)

      if (submit.get('queso')):
         print("Nombre ", nombre)
         print("Selecciono el queso")

         var = nombre
         enable1 = realizarmetodo(var)
         print(productos)
         print(lista)

      if (submit.get('Gomita')):
         print("Nombre ", nombre)
         print("Seleccionó la gomita")

         var = nombre
         enable2 = realizarmetodo(var)
         print(productos)
         print(lista)

      if (submit.get('Tocineta')):
         print("Nombre ", nombre)
         print("Seleccionó la adicion de tocineta")

         var = nombre
         enable3 = realizarmetodo(var)
         print(productos)
         print(lista)

   context = {

      'submit': submit,
      'enable': enable,
      'enable1': enable1,
      'enable2': enable2,
      'enable3': enable3,
   }

   return render(request, 'comida.html', context)

def realizarmetodo(var):

   return addCompra(var)

def buscarProducto(pProducto):

   encontrado = False
   if (pProducto in productos):

      # x = productos[pProducto]
      encontrado = True
      # print('Hay ', x, 'productos de: ', pProducto)
   else:

      encontrado = False
      # print('No hay productos')

   return encontrado

def addCompra(pProducto):
   cantidad = 0
   desactivado = True
   print(buscarProducto(pProducto))
   if buscarProducto(pProducto) == True:

      if productos[pProducto] > 0:

         if pProducto in lista:

            cant2 = productos[pProducto]
            print("Cantidad dos", cant2)
            productos[pProducto] = cant2 - 1

            if (productos[pProducto] == 0):
               desactivado = False

            cantidad = lista[pProducto]
            lista[pProducto] = cantidad + 1

         else:

            cant2 = productos[pProducto]
            print("Cantidad dos", cant2)
            productos[pProducto] = cant2 - 1
            print("Cantidad dos1", productos[pProducto])

            lista[pProducto] = cantidad + 1

      else:
         desactivado = False
         print('Se acabaron los producto')

   else:
      desactivado = False
      print('No puede agregar mas productos')
   return desactivado

def comida(request):
   return render(request, "comida.html")