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
    fecha_reserva = models.DateTimeField()
    cod_vendedor = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return '{} {}'.format(self.fecha_reserva, self.cod_vendedor)


class Venta(models.Model):
    # id_venta = models.UUIDField(primary_Key=True, default = uuid.uuid4)
    cant_producto = models.IntegerField()
    ced_vendedor = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return '{} {} {}'.format(self.cod_producto, self.ced_vendedor)


class Producto(models.Model):
    # id = models.UUIDField(primary_Key=True,  default=uuid.uuid4)
    valor_unitario = models.DecimalField(max_digits=15, decimal_places=3)
    nom_producto = models.CharField(max_length=20)
    cod_venta = models.ForeignKey(Venta, on_delete=models.CASCADE)
    imagen_producto = models.ImageField(upload_to='media')

    def __str__(self):
        return '{} {} {}'.format(self.valor_unitario, self.nom_producto, self.cod_venta)


class Cliente(models.Model):
    ced_cliente = models.IntegerField(primary_key=True, null=False)
    nom_cliente = models.CharField(max_length=30)
    correo_cliente = models.CharField(max_length=20)
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
    id = models.IntegerField(primary_key=True, null=False)
    nombre = models.CharField(max_length=50)
    numero_salas = models.IntegerField()

    def __str__(self):
        return '{} {}'.format(self.nombre, self.numero_salas)


class Pelicula(models.Model):
    id = models.IntegerField(primary_key=True, null=False)
    nom_pelicula = models.CharField(max_length=30)
    duracion_pelicula = models.CharField(max_length=30)
    CLASIFICACION = (
        ('AA', 'PUBLICO INFANTIL'),
        ('A', 'TODO PUBLICO'),
        ('B', 'ADOLESCENTES DE 12'),
        ('B15', 'ADOLESCENTES DE 15'),
        ('C', 'ADULTOS 18 AÑOS'),
        ('D', 'ADULTOS')
    )
    clasificacion = models.CharField(max_length=3, choices=CLASIFICACION)
    imagen_pelicula = models.ImageField(upload_to='media')
    trailer = models.URLField(blank=True)

    def __str__(self):
        return '{} {} {} {} {}'.format(self.nom_pelicula, self.duracion_pelicula, self.clasificacion,
                                       self.imagen_pelicula, self.trailer)


class Sala(models.Model):
    ESTADO_SALA = (
        ('HA', 'HABILITADA'),
        ('IN', 'INHABILITADA')
    )
    id = models.IntegerField(primary_key=True, null=False)
    cant_sillas = models.IntegerField()
    cod_multi = models.ForeignKey(Multiplex, on_delete=models.CASCADE)
    estado_sala = models.CharField(max_length=3, choices=ESTADO_SALA)

    def __str__(self):
        return '{} {} {}'.format(self.cant_sillas, self.cod_multi, self.estado_sala)


class Proyeccion(models.Model):
    id = models.IntegerField(primary_key=True, null=False)
    cod_sala = models.ForeignKey(Sala, on_delete=models.SET_NULL, null=True)
    cod_pelicula = models.ForeignKey(Pelicula, on_delete=models.SET_NULL, null=True)
    horario = models.DateTimeField()

    # def __str__(self):

    # return '{} {} {}'.format(self.cod_sala,self.cod_horario,self.cod_pelicula)


class Silla(models.Model):
    id = models.IntegerField(primary_key=True, null=False)
    cod_sala = models.ForeignKey(Sala, on_delete=models.CASCADE)
    TIPO_SILLA = (
        ('G', 'GENERAL'),
        ('P', 'PREFERENCIAL')
    )
    tipo_silla = models.CharField(max_length=1, choices=TIPO_SILLA)
    cod_reserva = models.ForeignKey(Reserva, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return '{} {} {}'.format(self.cod_sala, self.tipo_silla, self.cod_reserva)
