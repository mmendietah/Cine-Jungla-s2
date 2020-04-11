from django.db import models
from datetime import date
from django.contrib.auth.models import User
import uuid

class Registrado(models.Model):
    nombre = models.CharField(max_length=50)
    email = models.EmailField()

    def __str__(self):
        return self.nombre

class Reserva(models.Model):
    cod_reserva = models.UUIDField(primary_key=True, default=uuid.uuid4)
    fecha_reserva = models.DateTimeField(verbose_name="Fecha de reserva")
    cod_vendedor = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Vendedor")

    def __str__(self):
        return '{} {}'.format(self.fecha_reserva, self.cod_vendedor)


class Venta(models.Model):
    # id = models.UUIDField( default = uuid.uuid4)
    cant_producto = models.IntegerField(verbose_name="Cantidad de productos")
    ced_vendedor = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Vendedor")

    def __str__(self):
        return '{} {} {}'.format(self.cod_producto, self.ced_vendedor)


class Producto(models.Model):
    # id = models.UUIDField(default=uuid.uuid4)
    valor_unitario = models.DecimalField(max_digits=15, decimal_places=3, verbose_name="Valor unitario")
    nom_producto = models.CharField(max_length=20, verbose_name="Nombre del producto")
    cod_venta = models.ForeignKey(Venta, on_delete=models.CASCADE, verbose_name="codigo de venta")
    imagen_producto = models.ImageField(upload_to='media', verbose_name="imagen del producto")

    def __str__(self):
        return '{} {} {}'.format(self.valor_unitario, self.nom_producto, self.cod_venta)


class Cliente(models.Model):
    ced_cliente = models.IntegerField(primary_key=True, null=False, verbose_name="Cedula")
    nom_cliente = models.CharField(max_length=30, verbose_name="Nombre")
    correo_cliente = models.CharField(max_length=20, verbose_name="Correo")
    puntos_cliente = models.IntegerField()

    def __str__(self):
        return '{} {} {} {}'.format(self.ced_cliente, self.nom_cliente, self.correo_cliente, self.puntos_cliente)


class Factura(models.Model):
    cod_factura = models.UUIDField(primary_key=True, default=uuid.uuid4)
    TIPO_FACTURA = (
        ('RE', 'RESERVA'),
        ('PR', 'PRODUCTO')
    )
    tipo_factura = models.CharField(max_length=2, choices=TIPO_FACTURA)
    ced_cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    ced_vendedor = models.ForeignKey(User, on_delete=models.CASCADE)
    val_factura = models.DecimalField(max_digits=15, decimal_places=3)
    descripcion = models.CharField(max_length=50)

    def __str__(self):
        return '{} {} {} {} {}'.format(self.tipo_factura, self.ced_cliente, self.ced_vendedor, self.val_factura,
                                       self.descripcion)


# Create your models here.

class Multiplex(models.Model):
    id = models.IntegerField(primary_key=True, null=False, verbose_name="Codigo multiplex")
    nombre = models.CharField(max_length=50, verbose_name="Nombre")
    numero_salas = models.IntegerField(verbose_name="Número de salas")
    imagen_cc = models.ImageField(upload_to='media', verbose_name="Imagen cc", null=True)

    def __str__(self):
        return '{} -- {}'.format(self.id, self.nombre)


class Pelicula(models.Model):
    id = models.IntegerField(primary_key=True, null=False, verbose_name="Codigo película")
    nom_pelicula = models.CharField(max_length=30, verbose_name="Nombre")
    duracion_pelicula = models.TimeField(auto_now=False, auto_now_add=False, verbose_name="Duracion película")
    CLASIFICACION = (
        ('AA', 'PUBLICO INFANTIL'),
        ('A', 'TODO PUBLICO'),
        ('B', 'ADOLESCENTES DE 12'),
        ('B15', 'ADOLESCENTES DE 15'),
        ('C', 'ADULTOS 18 AÑOS'),
        ('D', 'ADULTOS')
    )
    clasificacion = models.CharField(max_length=3, choices=CLASIFICACION, verbose_name="Calsificación película")
    imagen_pelicula = models.ImageField(upload_to='media', verbose_name="Imagen película")
    trailer = models.URLField(blank=True, verbose_name="Trailer película")

    def __str__(self):
        return '{} -- {}'.format(self.id, self.nom_pelicula)


class Sala(models.Model):
    ESTADO_SALA = (
        ('HA', 'HABILITADA'),
        ('IN', 'INHABILITADA')
    )
    id = models.IntegerField(primary_key=True, null=False, verbose_name="Codigo sala")
    cant_sillas = models.IntegerField(verbose_name="Cantidad de sillas")
    cod_multi = models.ForeignKey(Multiplex, on_delete=models.CASCADE, verbose_name="Codigo múltiplex")
    estado_sala = models.CharField(max_length=3, choices=ESTADO_SALA, verbose_name="Estado sala")

    def __str__(self):
        return '{} -- {}'.format(self.id, self.cod_multi.nombre)


class Proyeccion(models.Model):
    id = models.IntegerField(primary_key=True, null=False, verbose_name="Codigo proyección")
    cod_sala = models.ForeignKey(Sala, on_delete=models.SET_NULL, null=True, verbose_name="Codigo Sala")
    cod_pelicula = models.ForeignKey(Pelicula, on_delete=models.SET_NULL, null=True, verbose_name="Codigo película")
    horario = models.DateTimeField(verbose_name="Hora película")

    def __str__(self):
        return '{} -- {} -- {}'.format(self.cod_pelicula.nom_pelicula, self.cod_sala.cod_multi.nombre, self.horario)


class Silla(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, verbose_name="Codigo silla")
    cod_sala = models.ForeignKey(Sala, on_delete=models.CASCADE, verbose_name="Codigo sala")
    TIPO_SILLA = (
        ('G', 'GENERAL'),
        ('P', 'PREFERENCIAL')
    )
    tipo_silla = models.CharField(max_length=1, choices=TIPO_SILLA, verbose_name="Tipo de silla")
    estado_silla = models.IntegerField(default=0, verbose_name="Estado silla")

    def __str__(self):
        return '{} -- {} -- {}'.format(self.cod_sala, self.tipo_silla, self.estado_silla)