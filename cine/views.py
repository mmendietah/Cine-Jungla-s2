from django.http import HttpResponse
from django.shortcuts import render, redirect
from .froms import addProd, regFrom, ProductoForm, actualizarProductoForm, actualizarListaForm
from .models import Multiplex, Silla, Pelicula, Proyeccion, Sala, Cliente, Producto, Venta, Lista, User
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as do_login
from django.contrib.auth import logout as do_logout
from django.contrib.auth.models import Group
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone

import os
from reportlab.platypus.tables import Table
from reportlab.lib import colors
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import SimpleDocTemplate, Paragraph, TableStyle
import reportlab
import MySQLdb

# from passlib.hash import pbkdf2_sha256

productos = {'combo 1': 5,
             'Queso': 2,
             'Gomita': 4,
             'Tocineta': 0,
             }
lista = {}

def nuevo(request):
   if request.method == "POST":
      nombre = request.POST['nombre']
      correo = request.POST['correo']
      cedula = request.POST['cedula']
      nuevo = Cliente.objects.create(ced_cliente=cedula,nom_cliente=nombre,correo_cliente=correo,puntos_cliente=0)
      nuevo.save()
      return logout(request)
   return render(request, "nuevo.html")

def confiteria(request):
   Lista.objects.all().delete()
   clientes = Cliente.objects.all()
   print(clientes)
   print("asdfafasdasdasdasdadasdasdsad")
   context= {
      'clientes': clientes
   }
   return render(request, "confiteria.html", context)

def peliculas(request):
   proyecciones = Proyeccion.objects.all()
   listap = []
   for proye in proyecciones:
      objeto = {'imagen_pelicula': "", 'peliId': 0, 'trailer': "",
                'nom_pelicula': "", 'duracion_pelicula': "",
                'clasificacion': "", 'salaId': 0, 'multiId': 0,
                'nombre': ""}
      peli = Pelicula.objects.get(id=proye.cod_pelicula_id)
      objeto['peliId'] = peli.id
      objeto['imagen_pelicula'] = peli.imagen_pelicula
      objeto['trailer'] = peli.trailer
      objeto['nom_pelicula'] = peli.nom_pelicula
      objeto['duracion_pelicula'] = peli.duracion_pelicula
      objeto['clasificacion'] = peli.clasificacion
      sala = Sala.objects.get(id=proye.cod_sala_id)
      objeto['salaId'] = sala.id
      multi = Multiplex.objects.get(id=sala.cod_multi_id)
      objeto['multiId'] = multi.id
      objeto['nombre'] = multi.nombre
      listap.append(objeto)
   context ={
      "listap": listap,
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
   clientes = Cliente.objects.all()
   pelicula = request.POST['p']
   sala = request.POST['s']
   sillas = Silla.objects.filter(cod_sala_id=sala)
   context = {
      "clientes": clientes,
      "sillas": sillas,
      "pelicula": pelicula,
      "multiplex": sala
   }
   return render(request, "asientos.html", context)

def comprar(request):
   if request.method == "POST":
      pag = request.POST['pag']
      silla1 = request.POST.getlist('id')
      multi = request.POST['s']
      peli = request.POST['p']
      ced = request.POST['cliente']
      if pag == 'C':
         cliente = Cliente.objects.get(ced_cliente=ced)
         pelicu = Pelicula.objects.get(id=peli)
         pelicula = pelicu.nom_pelicula
         salas = Sala.objects.get(id=multi)
         multiple = Multiplex.objects.get(id=salas.cod_multi_id)
         multiplex = multiple.nombre
         lista = []
         suma = 0
         int = 1
         boletas = 0
         for tipo in silla1:
            silla2 = Silla.objects.get(id=tipo)
            if silla2.tipo_silla == 'G':
               if cliente.puntos_cliente >= 100 and int == 1:
                  suma += (-11000)
                  int = 0
                  Cliente.objects.filter(ced_cliente=ced).update(puntos_cliente=0)
               suma += 11000
               boletas += 1
            else:
               suma += 15000
               boletas += 1
            lista.append(silla2)
         cliente = Cliente.objects.get(ced_cliente=ced)
         puntos = 10+(cliente.puntos_cliente)
         print(puntos)
         if cliente.nom_cliente != "Invitado":
            Cliente.objects.filter(ced_cliente=ced).update(puntos_cliente=puntos)
         context = {
            "lista": lista,
            "pelicula": pelicula,
            "multiplex": multiplex,
            "cliente": cliente,
            "total": suma
         }
         for silla in silla1:
            Silla.objects.filter(id = silla).update(estado_silla = 1)
         return render(request, "recibo.html", context)
      elif pag == 'R':
         for silla in silla1:
            Silla.objects.filter(id = silla).update(estado_silla = 2)
         sillas = Silla.objects.all()
         clientes = Cliente.objects.all()
         context = {
            "clientes": clientes,
            "sillas": sillas,
            "pelicula": peli,
            "multiplex": multi
         }
   return render(request, "asientos.html", context)

def inicio(request):
   if request.user.is_authenticated:
      Silla.objects.filter(estado_silla=2).update(estado_silla=0)
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
            return confiteria(request)
   return render(request, "registration/login.html")

# def login(request):
#    return render(request, "inicio.html")

def logout(request):
   do_logout(request)
   return redirect('../')

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

def indexConf(request):
   form = Producto.objects.all()
   listaForm = Lista.objects.all()
   ced = request.GET['cliente']
   cliente = Cliente.objects.get(ced_cliente=ced)
   cedUser = 2
   context = {'imgPrueba': form, 'cliente': cliente}
   if request.POST:
      val = request.POST
      rta = 0
      for i in val:
         rta = i
      if rta != 'combo1':
         productoData = Producto.objects.all().filter(id=rta)
         metodoNose(productoData)
      else:
         return ventaConfiteria(request, cedUser)
   context['listaForm'] = listaForm
   # CAMBIAR POR USUARIO
   if Lista.objects.filter(cod_usuario=cedUser).exists():
      context['enable'] = 'enable'

   return render(request, 'confiteria/indexConf.html', context)

def metodoNose(pProducto):
   producto = pProducto

   cantidadLista = 0
   id_p = 0
   for i in producto:
      id_p = i.id

   lista = Lista.objects.all().filter(id_producto=id_p)

   for datosProducto in producto:

      idProducto = datosProducto.id
      valorUnitario = datosProducto.valor_unitario
      nomProducto = datosProducto.nom_producto
      imagenProducto = datosProducto.imagen_producto
      cantidadProd = datosProducto.cant_producto

      if cantidadProd > 0:

         has = 0
         for ind in lista:
            has = ind.id_producto

         if datosProducto.id == has:

            cantidadProd = cantidadProd - 1

            updateProduct = Producto(id=idProducto, valor_unitario=valorUnitario, nom_producto=nomProducto,
                                     imagen_producto=imagenProducto, cant_producto=cantidadProd)

            form = actualizarProductoForm(instance=updateProduct)
            productData = form.save(commit=False)
            productData.save()

            cant = 0
            id_a = 0
            for j in lista:
               cant = j.cant_producto
               id_a = j.id

            cant = cant + 1

            # CAMBIAR CODIGO DE USUARIO
            updateLista = Lista(id=id_a, id_producto=idProducto, valor_unitario=valorUnitario, nom_producto=nomProducto,
                                imagen_producto=imagenProducto, cant_producto=cant, cod_usuario=2)

            formLista = actualizarListaForm(instance=updateLista)
            listData = formLista.save(commit=False)
            listData.save()
         else:

            cantidadProd = cantidadProd - 1
            updateProduct = Producto(id=idProducto, valor_unitario=valorUnitario, nom_producto=nomProducto,
                                     imagen_producto=imagenProducto, cant_producto=cantidadProd)

            form = actualizarProductoForm(instance=updateProduct)
            productData = form.save(commit=False)
            productData.save()
            cantidadLista = 1

            # CAMBIAR CODIGO DE USUARIO
            listaProducto = Lista(id_producto=idProducto, valor_unitario=valorUnitario, nom_producto=nomProducto,
                                  imagen_producto=imagenProducto, cant_producto=cantidadLista, cod_usuario=2)
            listaProducto.save()

def ventaConfiteria(request, pCedvendedor):
   form = Lista.objects.filter(cod_usuario=pCedvendedor)
   ced = request.GET['cliente']
   cliente = Cliente.objects.get(ced_cliente=ced)
   vendedor = User.objects.get(id=pCedvendedor)
   suma = 0
   for producto in form:
      c = producto.cant_producto
      v = producto.valor_unitario
      suma += c*v
   context = {
      'lista': form,
      'cliente': cliente,
      'vendedor': vendedor,
      'total': suma
   }
   return render(request, 'confiteria/ventaConf.html', context)

def prueba(request):
   if request.method == 'POST':
      form = ProductoForm(request.POST, request.FILES)
      if (form.is_valid()):
         form.save()

         return listarProductos(request)
   else:

      form = ProductoForm()

   return render(request, 'confiteria/prueba.html', {'form': form})

def listarProductos(request):
   form = Producto.objects.all()
   context = {

      'imgPrueba': form
   }

   return render(request, 'confiteria/listPrueba.html', context)

def comprarComida(request):
   if request.method == "POST":
      productos = request.POST.getlist('id')
      total = request.POST.get('total')
      cedula = request.POST.get('ced')
      clie = request.POST.get('cedula')
      cliente = Cliente.objects.get(ced_cliente=clie)
      puntos = 5 + (cliente.puntos_cliente)
      if cliente.nom_cliente != "Invitado":
         Cliente.objects.filter(ced_cliente=clie).update(puntos_cliente=puntos)
      cantidad = 0
      cod = 0
      for product in productos:
         produc = Lista.objects.get(id=product)
         cantidad += produc.cant_producto
         cod = produc.id_producto
      venta = Venta.objects.create(cant_producto=cantidad,ced_vendedor_id=cedula,cod_producto_id=cod,
                                   fecha_venta=timezone.now(),valor_venta=total)
      venta.save()
   return confiteria(request)


def reportes(request):
   if request.user.is_authenticated:
      response = HttpResponse(content_type='cineJungla/pdf')
      response['Content-Disposition'] = 'attachment; filename = Cine-ventas-report.pdf'
      buffer = BytesIO()
      c = canvas.Canvas(buffer, pagesize=A4)

      c.setLineWidth(.3)
      c.setFont('Helvetica', 22)
      c.drawString(30, 750, 'Cine Jungla')
      c.setFont('Helvetica', 12)
      c.drawString(30, 735, 'Reporte')
      c.setFont('Helvetica-Bold', 12)
      c.drawString(480, 750, "2020")
      c.line(460, 747, 560, 747)

      db = MySQLdb.connect(user='YpwDdtMdT2', db='YpwDdtMdT2', passwd='GkCUCMa0XN', host='remotemysql.com')
      cursor = db.cursor()
      cursor.execute('select nombre, SUM(val_factura) from cine_factura, auth_user, cine_reserva, cine_silla, cine_sala, cine_multiplex where cine_multiplex.id = cine_sala.cod_multi_id and cine_silla.cod_sala_id = cine_sala.id and cine_reserva.cod_reserva = cine_silla.reser_id and auth_user.id = cine_reserva.cod_vendedor_id and cine_factura.ced_vendedor_id = auth_user.id Group BY (nombre)')
      names = [row for row in cursor.fetchall()]
      db.close()

      styles = getSampleStyleSheet()
      styleBH = styles["Normal"]
      styleBH.alignment = TA_CENTER
      styleBH.fontSize = 10

      numero = Paragraph('''No.''', styleBH)
      multi = Paragraph('''Multiplex''', styleBH)
      total = Paragraph('''Total''', styleBH)

      data = []
      data.append([numero, multi, total])

      styleN = styles["BodyText"]
      styleN.alignment = TA_CENTER
      styleN.fontSize = 7

      width, height = A4
      high = 650
      cont = 1
      for dato in names:
         mul = [cont, dato[0], dato[1]]
         data.append(mul)
         high = high - 18
         cont += 1

      width, height = A4
      table = Table(data, colWidths=[1.9 * cm, 6.5 * cm, 1.9 * cm, 1.9 * cm, 1.9 * cm, 1.9 * cm])
      table.setStyle(TableStyle([
         ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
         ('BOX', (0, 0), (-1, -1), 0.25, colors.black), ]))

      table.wrapOn(c, width, height)
      table.drawOn(c, 30, high)
      c.showPage()

      c.save()

      pdf = buffer.getvalue()
      buffer.close()
      response.write(pdf)
      return response
   else:
      return redirect('/admin')