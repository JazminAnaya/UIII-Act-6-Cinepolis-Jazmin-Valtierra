# app_Cinepolis/models.py
from django.db import models
from django.utils import timezone # Importar para fecha_hora de transacción

# ===================
# MODELO: Sucursal
# ===================
class Sucursal(models.Model):
    ESTADOS = [
        ('activo', 'Activo'),
        ('cerrado', 'Cerrado'),
        ('mantenimiento', 'Mantenimiento'),
    ]
    FORMATOS = [
        ('tradicional', 'Tradicional'),
        ('3D', '3D'),
        ('4DX', '4DX'),
        ('VIP', 'VIP'),
        ('IMAX', 'IMAX'),
        ('JUNIOR', 'Junior'),
    ]
    id_sucursal = models.AutoField(primary_key=True)
    nombre_cine = models.CharField(max_length=100)
    direccion = models.CharField(max_length=200)
    ciudad = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20)
    numero_salas = models.IntegerField()
    estado = models.CharField(max_length=20, choices=ESTADOS, default='activo')
    formatos = models.CharField(max_length=20, choices=FORMATOS, default='tradicional')

    def __str__(self):
        return f"{self.nombre_cine} - {self.ciudad}"

# ============================================
# MODELO: Sala
# ============================================
class Sala(models.Model):
    TIPOS_SALA = [
        ('Tradicional', 'Tradicional'),
        ('3D', '3D'),
        ('4DX', '4DX'),
        ('VIP', 'VIP'),
        ('IMAX', 'IMAX'),
        ('JUNIOR', 'Junior'),
    ]
    ESTADOS_SALA = [
        ('Ocupada', 'Ocupada'),
        ('Desocupada', 'Desocupada'),
        ('En mantenimiento', 'En mantenimiento'),
    ]
    id_sala = models.AutoField(primary_key=True)
    numero_sala = models.IntegerField()
    tipo_sala = models.CharField(max_length=20, choices=TIPOS_SALA, default='Tradicional')
    capacidad = models.IntegerField()
    estado = models.CharField(max_length=20, choices=ESTADOS_SALA, default='Desocupada')
    fecha_ultimo_mantenimiento = models.DateField()
    asientos_especiales = models.IntegerField()

    # Relación 1 a muchos: una sucursal puede tener muchas salas
    sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE, related_name='salas')

    def __str__(self):
        return f"Sala {self.numero_sala} - {self.tipo_sala} ({self.sucursal.nombre_cine})"

# ============================================
# MODELO: Pelicula
# ============================================
class Pelicula(models.Model):
    id_pelicula = models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=200)
    genero = models.CharField(max_length=100)
    clasificacion = models.CharField(max_length=100)
    duracion = models.IntegerField(help_text="Duración en minutos")
    sinopsis = models.TextField()
    director = models.CharField(max_length=150)

    # Relación muchos a muchos: una sala puede tener varias películas y viceversa
    salas = models.ManyToManyField(Sala, related_name='peliculas')

    def __str__(self):
        return self.titulo

        # ============================================
# MODELO: Funcion
# ============================================
class Funcion(models.Model):
    IDIOMAS = [
        ('Español', 'Español'),
        ('Ingles', 'Inglés'),
        ('Subtitulada', 'Subtitulada'),
    ]
    ESTATUS = [
        ('Programada', 'Programada'),
        ('Cancelada', 'Cancelada'),
        ('Finalizada', 'Finalizada'),
    ]
    id_funcion = models.AutoField(primary_key=True)
    pelicula = models.ForeignKey(Pelicula, on_delete=models.CASCADE, related_name='funciones')
    sala = models.ForeignKey(Sala, on_delete=models.CASCADE, related_name='funciones')
    sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE, related_name='funciones') # Redundante pero solicitado
    fecha_hora = models.DateTimeField()
    precio_boleto = models.DecimalField(max_digits=5, decimal_places=2)
    idioma = models.CharField(max_length=20, choices=IDIOMAS, default='Español')
    estatus = models.CharField(max_length=20, choices=ESTATUS, default='Programada')

    def __str__(self):
        return f"{self.pelicula.titulo} - Sala {self.sala.numero_sala} ({self.sucursal.nombre_cine}) - {self.fecha_hora.strftime('%d/%m/%Y %H:%M')}"

# ============================================
# MODELO: Cliente
# ============================================
class Cliente(models.Model):
    MEMBRESIAS = [
        ('Tradicional', 'Tradicional'),
        ('Premium', 'Premium'),
        ('Club CinépolisFan', 'Club Cinépolis Fan'),
        ('Club Cinépolis Fanático', 'Club Cinépolis Fanático'),
        ('Club Cinépolis Súper Fanático', 'Club Cinépolis Súper Fanático'),
    ]
    id_cliente = models.AutoField(primary_key=True) # Cambiado a AutoField por ser PK
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(unique=True)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    puntos_cinepolis = models.IntegerField(default=0)
    membresia_cinepolis = models.CharField(max_length=30, choices=MEMBRESIAS, default='Tradicional')

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

# ============================================
# MODELO: Transaccion
# ============================================
class Transaccion(models.Model):
    METODOS_PAGO = [
        ('Tarjeta de Credito', 'Tarjeta de Crédito'),
        ('Tarjeta de Debito', 'Tarjeta de Débito'),
        ('Efectivo', 'Efectivo'),
        ('Puntos Cinepolis', 'Puntos Cinépolis'),
    ]
    id_transaccion = models.AutoField(primary_key=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='transacciones')
    funcion = models.ForeignKey(Funcion, on_delete=models.CASCADE, related_name='transacciones')
    fecha_hora_compra = models.DateTimeField(default=timezone.now)
    cantidad_boletos = models.IntegerField() # Cambiado a IntegerField para boletos
    # precio_boleto ya está en Funcion, no es una FK de Transaccion a precio_boleto de Funcion
    # Se debe capturar el precio al momento de la transacción o referenciarlo via funcion
    precio_boleto_momento_compra = models.DecimalField(max_digits=5, decimal_places=2) # Para guardar el precio en el momento de la compra
    monto_total = models.DecimalField(max_digits=8, decimal_places=2, editable=False) # Se calculará automáticamente
    metodo_pago = models.CharField(max_length=25, choices=METODOS_PAGO, default='Tarjeta de Credito')

    def save(self, *args, **kwargs):
        # Calcular monto_total antes de guardar
        self.monto_total = self.cantidad_boletos * self.precio_boleto_momento_compra
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Transacción #{self.id_transaccion} - {self.cliente.nombre} - {self.funcion.pelicula.titulo}"