from django.shortcuts import render
from .froms import RegFrom, RegModelForm, ContactForm, addProd
from .models import Registrado

# -------------------------------------------
#     Desde acá
# -------------------------------------------

productos = {'combo 1': 5,
             'Queso': 2,
             'Gomita': 4,
             'Tocineta': 0,
             }
lista = {}

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

def inicio(request):
   return render(request, "inicio.html")

def crud(request):
   registros = Registrado.objects.all()
   context = {
      'registros': registros
   }
   return render(request, "CRUD.html", context)

def login(request):
   return render(request, "registration/login.html", {})

def asientos(request):
   return render(request, "asientos.html")

def comida(request):
   # form = CarritoForm(request.POST or None)
   # pag = PagForm(request.POST)
   # if pag.is_valid():
   #    nompag = pag.cleaned_data.get("pag")
   #    if nompag == 'pagar' and form.is_valid():
   #       context = {
   #          "el_form": form,
   #       }
   #       return render(request, "pagar.html", context)
   #    if nompag == 'comida':
   #       context = {
   #          "form": form,
   #       }
   #       return render(request, "comida.html", context)
   # context = {
   #    "form": form,
   # }
   return render(request, "comida.html")

def contact(request):
   form = ContactForm(request.POST or None)
   # if form.is_valid():
   #    form_email = form.cleaned_data.get("email")
   #    form_mensaje = form.cleaned_data.get("mensaje")
   #    form_nombre = form.cleaned_data.get("nombre")
      # asunto = 'From de Contacto'
      # email_from = settings.EMAIL_HOST_USER
      # email_to = [email_from, "miguemh99@gmail.com"]
      # email_mensaje = "%s: %s enviado por %s" %(form_nombre, form_mensaje, form_email)
      # send_mail(asunto,
      #     email_mensaje,
      #     email_from,
      #     email_to,
      #     # [email_to],
      #     fail_silently=False
      #     )
      # for key in form.cleaned_data:
      #    print(key)
      #    print(form.cleaned_data.get(key))
   context = {
      "el_form": form,
   }
   return render(request,"inicio.html", context)

def inicio(request):
   titulo = "Hola"
   #if request.user.is_authenticated():
   #   titulo = "que mas %s" %(request.user)
   #form = RegForm(request.POST or None)
   form = RegModelForm(request.POST or None)
   #print(dir(form))

   context = {
      "titulo": titulo,
      "el_form": form,
   }

   if form.is_valid():
      instance = form.save(commit=False)
      nombre = form.cleaned_data.get("nombre")
      if instance.nombre == "Miguel":
         context = {
            "titulo": "gracias %s!" %(nombre)
         }
      # instance.save()
      print(instance)
      # print(instance.timestamp)
         # form_date = form.cleaned_data
         # n = form_date.get("nombre")
         # c = form_date.get("clave")
         # obj = Usuario.objects.create(nombre=n, clave=c)

   return render(request,"inicio.html", context)

def inicio3(request):
   titulo = "HOLA"
   if request.user.is_authenticated:
      titulo = "Bienvenido %s" %(request.user)
   form = RegFrom(request.POST or None)
   # print(dir(form))
   if form.is_valid():
      form_data = form.cleaned_data
      abc = form_data.get("email")
      asd = form_data.get("nombre")
      obj = Registrado.objects.create(nombre=asd,email=abc)
   context = {
      "titulo": titulo,
      "el_form": form,
   }
   return render(request, "inicio.html", context)

def inicio2(request):
   form = RegFrom(request.POST or None)
   # print(dir(form))
   if form.is_valid():
      nombre = form.cleaned_data.get("nombre")
      print(nombre)
   context = {
      "el_form": form,
   }
   return render(request, "inicio.html", context)

def inicio1(request):
   form = RegFrom()
   context = {
      "el_form": form,
   }
   return render(request,"inicio.html", context)