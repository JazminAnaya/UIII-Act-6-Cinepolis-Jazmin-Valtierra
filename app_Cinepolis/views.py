
# app_Cinepolis/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Sucursal, Sala, Pelicula, Funcion, Cliente, Transaccion # Importa todos los modelos
from datetime import datetime # Para manejar la fecha y hora
from django.utils import timezone # Para fecha_hora_compra

# Función para la página de inicio
def inicio_cinepolis(request):
    return render(request, 'inicio.html')

# Función para agregar una sucursal
def agregar_sucursal(request):
    if request.method == 'POST':
        nombre_cine = request.POST.get('nombre_cine')
        direccion = request.POST.get('direccion')
        ciudad = request.POST.get('ciudad')
        telefono = request.POST.get('telefono')
        numero_salas = request.POST.get('numero_salas')
        estado = request.POST.get('estado')
        formatos = request.POST.get('formatos')

        Sucursal.objects.create(
            nombre_cine=nombre_cine,
            direccion=direccion,
            ciudad=ciudad,
            telefono=telefono,
            numero_salas=numero_salas,
            estado=estado,
            formatos=formatos
        )
        return redirect('ver_sucursales')
    return render(request, 'sucursal/agregar_sucursal.html')

# Función para ver todas las sucursales
def ver_sucursales(request):
    sucursales = Sucursal.objects.all()
    return render(request, 'sucursal/ver_sucursales.html', {'sucursales': sucursales})

# Función para mostrar el formulario de actualización de una sucursal
def actualizar_sucursal(request, pk):
    sucursal = get_object_or_404(Sucursal, pk=pk)
    return render(request, 'sucursal/actualizar_sucursal.html', {'sucursal': sucursal})

# Función para realizar la actualización de una sucursal
def realizar_actualizacion_sucursal(request, pk):
    sucursal = get_object_or_404(Sucursal, pk=pk)
    if request.method == 'POST':
        sucursal.nombre_cine = request.POST.get('nombre_cine')
        sucursal.direccion = request.POST.get('direccion')
        sucursal.ciudad = request.POST.get('ciudad')
        sucursal.telefono = request.POST.get('telefono')
        sucursal.numero_salas = request.POST.get('numero_salas')
        sucursal.estado = request.POST.get('estado')
        sucursal.formatos = request.POST.get('formatos')
        sucursal.save()
        return redirect('ver_sucursales')
    return render(request, 'sucursal/actualizar_sucursal.html', {'sucursal': sucursal})


# Función para borrar una sucursal
def borrar_sucursal(request, pk):
    sucursal = get_object_or_404(Sucursal, pk=pk)
    if request.method == 'POST':
        sucursal.delete()
        return redirect('ver_sucursales')
    return render(request, 'sucursal/borrar_sucursal.html', {'sucursal': sucursal})


# Función para agregar una sala
def agregar_sala(request):
    sucursales = Sucursal.objects.all() # Necesitamos las sucursales para el dropdown
    if request.method == 'POST':
        numero_sala = request.POST.get('numero_sala')
        tipo_sala = request.POST.get('tipo_sala')
        capacidad = request.POST.get('capacidad')
        estado = request.POST.get('estado')
        fecha_ultimo_mantenimiento_str = request.POST.get('fecha_ultimo_mantenimiento')
        asientos_especiales = request.POST.get('asientos_especiales')
        sucursal_id = request.POST.get('sucursal')

        sucursal_obj = get_object_or_404(Sucursal, pk=sucursal_id)
        fecha_mantenimiento = datetime.strptime(fecha_ultimo_mantenimiento_str, '%Y-%m-%d').date()

        Sala.objects.create(
            numero_sala=numero_sala,
            tipo_sala=tipo_sala,
            capacidad=capacidad,
            estado=estado,
            fecha_ultimo_mantenimiento=fecha_mantenimiento,
            asientos_especiales=asientos_especiales,
            sucursal=sucursal_obj
        )
        return redirect('ver_salas')
    return render(request, 'sala/agregar_sala.html', {'sucursales': sucursales})

# Función para ver todas las salas
def ver_salas(request):
    salas = Sala.objects.all().select_related('sucursal').order_by('sucursal__nombre_cine', 'numero_sala')
    return render(request, 'sala/ver_salas.html', {'salas': salas})

# Función para mostrar el formulario de actualización de una sala
def actualizar_sala(request, pk):
    sala = get_object_or_404(Sala, pk=pk)
    sucursales = Sucursal.objects.all()
    return render(request, 'sala/actualizar_sala.html', {'sala': sala, 'sucursales': sucursales})

# Función para realizar la actualización de una sala
def realizar_actualizacion_sala(request, pk):
    sala = get_object_or_404(Sala, pk=pk)
    if request.method == 'POST':
        sala.numero_sala = request.POST.get('numero_sala')
        sala.tipo_sala = request.POST.get('tipo_sala')
        sala.capacidad = request.POST.get('capacidad')
        sala.estado = request.POST.get('estado')
        fecha_ultimo_mantenimiento_str = request.POST.get('fecha_ultimo_mantenimiento')
        sala.fecha_ultimo_mantenimiento = datetime.strptime(fecha_ultimo_mantenimiento_str, '%Y-%m-%d').date()
        sala.asientos_especiales = request.POST.get('asientos_especiales')
        sucursal_id = request.POST.get('sucursal')
        sala.sucursal = get_object_or_404(Sucursal, pk=sucursal_id)
        sala.save()
        return redirect('ver_salas')
    return render(request, 'sala/actualizar_sala.html', {'sala': sala, 'sucursales': Sucursal.objects.all()})

# Función para borrar una sala
def borrar_sala(request, pk):
    sala = get_object_or_404(Sala, pk=pk)
    if request.method == 'POST':
        sala.delete()
        return redirect('ver_salas')
    return render(request, 'sala/borrar_sala.html', {'sala': sala})

# Función para agregar una película
def agregar_pelicula(request):
    salas = Sala.objects.all().select_related('sucursal').order_by('sucursal__nombre_cine', 'numero_sala')
    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        genero = request.POST.get('genero')
        clasificacion = request.POST.get('clasificacion')
        duracion = request.POST.get('duracion')
        sinopsis = request.POST.get('sinopsis')
        director = request.POST.get('director')
        salas_seleccionadas_ids = request.POST.getlist('salas') # Obtener una lista de IDs

        pelicula = Pelicula.objects.create(
            titulo=titulo,
            genero=genero,
            clasificacion=clasificacion,
            duracion=duracion,
            sinopsis=sinopsis,
            director=director
        )
        # Asignar salas a la película
        if salas_seleccionadas_ids:
            pelicula.salas.set(salas_seleccionadas_ids) # Usa .set() para ManyToMany

        return redirect('ver_peliculas')
    return render(request, 'pelicula/agregar_pelicula.html', {'salas': salas})

# Función para ver todas las películas
def ver_peliculas(request):
    peliculas = Pelicula.objects.all().prefetch_related('salas__sucursal')
    return render(request, 'pelicula/ver_peliculas.html', {'peliculas': peliculas})

# Función para mostrar el formulario de actualización de una película
def actualizar_pelicula(request, pk):
    pelicula = get_object_or_404(Pelicula, pk=pk)
    salas = Sala.objects.all().select_related('sucursal').order_by('sucursal__nombre_cine', 'numero_sala')
    salas_asignadas_ids = pelicula.salas.values_list('id_sala', flat=True) # Obtener IDs de salas ya asignadas

    return render(request, 'pelicula/actualizar_pelicula.html', {
        'pelicula': pelicula,
        'salas': salas,
        'salas_asignadas_ids': list(salas_asignadas_ids)
    })

# Función para realizar la actualización de una película
def realizar_actualizacion_pelicula(request, pk):
    pelicula = get_object_or_404(Pelicula, pk=pk)
    if request.method == 'POST':
        pelicula.titulo = request.POST.get('titulo')
        pelicula.genero = request.POST.get('genero')
        pelicula.clasificacion = request.POST.get('clasificacion')
        pelicula.duracion = request.POST.get('duracion')
        pelicula.sinopsis = request.POST.get('sinopsis')
        pelicula.director = request.POST.get('director')
        pelicula.save()

        salas_seleccionadas_ids = request.POST.getlist('salas')
        pelicula.salas.set(salas_seleccionadas_ids) # Actualiza las salas asociadas

        return redirect('ver_peliculas')
    return render(request, 'pelicula/actualizar_pelicula.html', {'pelicula': pelicula, 'salas': Sala.objects.all()})

# Función para borrar una película
def borrar_pelicula(request, pk):
    pelicula = get_object_or_404(Pelicula, pk=pk)
    if request.method == 'POST':
        pelicula.delete()
        return redirect('ver_peliculas')
    return render(request, 'pelicula/borrar_pelicula.html', {'pelicula': pelicula})

# ============================================
# FUNCIONES PARA EL MODELO: Funcion
# ============================================

def agregar_funcion(request):
    peliculas = Pelicula.objects.all().order_by('titulo')
    salas = Sala.objects.all().select_related('sucursal').order_by('sucursal__nombre_cine', 'numero_sala')
    sucursales = Sucursal.objects.all().order_by('nombre_cine')
    
    # Pasar las opciones de choices al contexto
    idiomas_opciones = Funcion.IDIOMAS
    estatus_opciones = Funcion.ESTATUS
    
    if request.method == 'POST':
        pelicula_id = request.POST.get('pelicula')
        sala_id = request.POST.get('sala')
        sucursal_id = request.POST.get('sucursal')
        fecha_hora_str = request.POST.get('fecha_hora')
        precio_boleto = request.POST.get('precio_boleto')
        idioma = request.POST.get('idioma')
        estatus = request.POST.get('estatus')

        # Convertir precio_boleto a float
        try:
            precio_boleto = float(precio_boleto)
        except (ValueError, TypeError):
            return render(request, 'funcion/agregar_funcion.html', {
                'peliculas': peliculas,
                'salas': salas,
                'sucursales': sucursales,
                'idiomas_opciones': idiomas_opciones,
                'estatus_opciones': estatus_opciones,
                'error': 'Por favor ingrese un precio válido.'
            })

        pelicula_obj = get_object_or_404(Pelicula, pk=pelicula_id)
        sala_obj = get_object_or_404(Sala, pk=sala_id)
        sucursal_obj = get_object_or_404(Sucursal, pk=sucursal_id)
        fecha_hora_obj = datetime.strptime(fecha_hora_str, '%Y-%m-%dT%H:%M')

        Funcion.objects.create(
            pelicula=pelicula_obj,
            sala=sala_obj,
            sucursal=sucursal_obj,
            fecha_hora=fecha_hora_obj,
            precio_boleto=precio_boleto,
            idioma=idioma,
            estatus=estatus
        )
        return redirect('ver_funciones')
    
    return render(request, 'funcion/agregar_funcion.html', {
        'peliculas': peliculas,
        'salas': salas,
        'sucursales': sucursales,
        'idiomas_opciones': idiomas_opciones,
        'estatus_opciones': estatus_opciones
    })

def ver_funciones(request):
    funciones = Funcion.objects.all().select_related('pelicula', 'sala__sucursal', 'sucursal').order_by('fecha_hora')
    return render(request, 'funcion/ver_funciones.html', {'funciones': funciones})

def actualizar_funcion(request, pk):
    funcion = get_object_or_404(Funcion, pk=pk)
    peliculas = Pelicula.objects.all().order_by('titulo')
    salas = Sala.objects.all().select_related('sucursal').order_by('sucursal__nombre_cine', 'numero_sala')
    sucursales = Sucursal.objects.all().order_by('nombre_cine')
    
    # Pasar las opciones de choices al contexto
    idiomas_opciones = Funcion.IDIOMAS
    estatus_opciones = Funcion.ESTATUS
    
    if request.method == 'POST':
        funcion.pelicula = get_object_or_404(Pelicula, pk=request.POST.get('pelicula'))
        funcion.sala = get_object_or_404(Sala, pk=request.POST.get('sala'))
        funcion.sucursal = get_object_or_404(Sucursal, pk=request.POST.get('sucursal'))
        fecha_hora_str = request.POST.get('fecha_hora')
        funcion.fecha_hora = datetime.strptime(fecha_hora_str, '%Y-%m-%dT%H:%M')
        
        # Convertir precio_boleto a float
        try:
            funcion.precio_boleto = float(request.POST.get('precio_boleto'))
        except (ValueError, TypeError):
            return render(request, 'funcion/actualizar_funcion.html', {
                'funcion': funcion,
                'peliculas': peliculas,
                'salas': salas,
                'sucursales': sucursales,
                'idiomas_opciones': idiomas_opciones,
                'estatus_opciones': estatus_opciones,
                'error': 'Por favor ingrese un precio válido.'
            })
        
        funcion.idioma = request.POST.get('idioma')
        funcion.estatus = request.POST.get('estatus')
        funcion.save()
        return redirect('ver_funciones')
    
    return render(request, 'funcion/actualizar_funcion.html', {
        'funcion': funcion,
        'peliculas': peliculas,
        'salas': salas,
        'sucursales': sucursales,
        'idiomas_opciones': idiomas_opciones,
        'estatus_opciones': estatus_opciones
    })

def borrar_funcion(request, pk):
    funcion = get_object_or_404(Funcion, pk=pk)
    if request.method == 'POST':
        funcion.delete()
        return redirect('ver_funciones')
    return render(request, 'funcion/borrar_funcion.html', {'funcion': funcion})

# ============================================
# FUNCIONES PARA EL MODELO: Cliente
# ============================================

def agregar_cliente(request):
    # Pasar las opciones de choices al contexto
    membresias_opciones = Cliente.MEMBRESIAS
    
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        telefono = request.POST.get('telefono')
        email = request.POST.get('email')
        fecha_nacimiento_str = request.POST.get('fecha_nacimiento')
        puntos_cinepolis = request.POST.get('puntos_cinepolis')
        membresia_cinepolis = request.POST.get('membresia_cinepolis')

        # Convertir puntos_cinepolis a entero
        try:
            puntos_cinepolis = int(puntos_cinepolis)
        except (ValueError, TypeError):
            puntos_cinepolis = 0

        fecha_nacimiento = datetime.strptime(fecha_nacimiento_str, '%Y-%m-%d').date() if fecha_nacimiento_str else None

        Cliente.objects.create(
            nombre=nombre,
            apellido=apellido,
            telefono=telefono,
            email=email,
            fecha_nacimiento=fecha_nacimiento,
            puntos_cinepolis=puntos_cinepolis,
            membresia_cinepolis=membresia_cinepolis
        )
        return redirect('ver_clientes')
    
    return render(request, 'cliente/agregar_cliente.html', {
        'membresias_opciones': membresias_opciones
    })

def ver_clientes(request):
    clientes = Cliente.objects.all().order_by('apellido', 'nombre')
    return render(request, 'cliente/ver_clientes.html', {'clientes': clientes})

def actualizar_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    
    # Pasar las opciones de choices al contexto
    membresias_opciones = Cliente.MEMBRESIAS
    
    if request.method == 'POST':
        cliente.nombre = request.POST.get('nombre')
        cliente.apellido = request.POST.get('apellido')
        cliente.telefono = request.POST.get('telefono')
        cliente.email = request.POST.get('email')
        fecha_nacimiento_str = request.POST.get('fecha_nacimiento')
        cliente.fecha_nacimiento = datetime.strptime(fecha_nacimiento_str, '%Y-%m-%d').date() if fecha_nacimiento_str else None
        
        # Convertir puntos_cinepolis a entero
        try:
            cliente.puntos_cinepolis = int(request.POST.get('puntos_cinepolis'))
        except (ValueError, TypeError):
            cliente.puntos_cinepolis = cliente.puntos_cinepolis  # Mantener el valor actual
        
        cliente.membresia_cinepolis = request.POST.get('membresia_cinepolis')
        cliente.save()
        return redirect('ver_clientes')
    
    return render(request, 'cliente/actualizar_cliente.html', {
        'cliente': cliente,
        'membresias_opciones': membresias_opciones
    })

def borrar_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        cliente.delete()
        return redirect('ver_clientes')
    return render(request, 'cliente/borrar_cliente.html', {'cliente': cliente})

# ============================================
# FUNCIONES PARA EL MODELO: Transaccion
# ============================================

def agregar_transaccion(request):
    clientes = Cliente.objects.all().order_by('apellido', 'nombre')
    funciones = Funcion.objects.all().select_related('pelicula', 'sala__sucursal').order_by('fecha_hora')
    
    # Pasar las opciones de choices al contexto
    metodos_pago_opciones = Transaccion.METODOS_PAGO
    
    if request.method == 'POST':
        cliente_id = request.POST.get('cliente')
        funcion_id = request.POST.get('funcion')
        cantidad_boletos = request.POST.get('cantidad_boletos')
        precio_boleto_momento_compra = request.POST.get('precio_boleto_momento_compra')
        metodo_pago = request.POST.get('metodo_pago')

        # CONVERTIR LOS VALORES A LOS TIPOS CORRECTOS
        try:
            cantidad_boletos = int(cantidad_boletos)
            precio_boleto_momento_compra = float(precio_boleto_momento_compra)
        except (ValueError, TypeError):
            # Manejar error de conversión
            return render(request, 'transaccion/agregar_transaccion.html', {
                'clientes': clientes,
                'funciones': funciones,
                'metodos_pago_opciones': metodos_pago_opciones,
                'error': 'Por favor ingrese valores válidos para cantidad de boletos y precio.'
            })

        cliente_obj = get_object_or_404(Cliente, pk=cliente_id)
        funcion_obj = get_object_or_404(Funcion, pk=funcion_id)

        Transaccion.objects.create(
            cliente=cliente_obj,
            funcion=funcion_obj,
            cantidad_boletos=cantidad_boletos,
            precio_boleto_momento_compra=precio_boleto_momento_compra,
            metodo_pago=metodo_pago
        )
        return redirect('ver_transacciones')
    
    return render(request, 'transaccion/agregar_transaccion.html', {
        'clientes': clientes,
        'funciones': funciones,
        'metodos_pago_opciones': metodos_pago_opciones
    })

def ver_transacciones(request):
    # Ordenar por ID de transacción (ascendente)
    transacciones = Transaccion.objects.all().select_related('cliente', 'funcion__pelicula', 'funcion__sala__sucursal').order_by('id_transaccion')
    return render(request, 'transaccion/ver_transacciones.html', {'transacciones': transacciones})

def actualizar_transaccion(request, pk):
    transaccion = get_object_or_404(Transaccion, pk=pk)
    clientes = Cliente.objects.all().order_by('apellido', 'nombre')
    funciones = Funcion.objects.all().select_related('pelicula', 'sala__sucursal').order_by('fecha_hora')
    
    # Pasar las opciones de choices al contexto
    metodos_pago_opciones = Transaccion.METODOS_PAGO
    
    if request.method == 'POST':
        transaccion.cliente = get_object_or_404(Cliente, pk=request.POST.get('cliente'))
        transaccion.funcion = get_object_or_404(Funcion, pk=request.POST.get('funcion'))
        
        # CONVERTIR LOS VALORES A LOS TIPOS CORRECTOS
        try:
            cantidad_boletos = int(request.POST.get('cantidad_boletos'))
            precio_boleto_momento_compra = float(request.POST.get('precio_boleto_momento_compra'))
        except (ValueError, TypeError):
            # Manejar error de conversión
            return render(request, 'transaccion/actualizar_transaccion.html', {
                'transaccion': transaccion,
                'clientes': clientes,
                'funciones': funciones,
                'metodos_pago_opciones': metodos_pago_opciones,
                'error': 'Por favor ingrese valores válidos para cantidad de boletos y precio.'
            })
        
        transaccion.cantidad_boletos = cantidad_boletos
        transaccion.precio_boleto_momento_compra = precio_boleto_momento_compra
        transaccion.metodo_pago = request.POST.get('metodo_pago')
        transaccion.save()
        return redirect('ver_transacciones')
    
    return render(request, 'transaccion/actualizar_transaccion.html', {
        'transaccion': transaccion,
        'clientes': clientes,
        'funciones': funciones,
        'metodos_pago_opciones': metodos_pago_opciones
    })

def borrar_transaccion(request, pk):
    transaccion = get_object_or_404(Transaccion, pk=pk)
    if request.method == 'POST':
        transaccion.delete()
        return redirect('ver_transacciones')
    return render(request, 'transaccion/borrar_transaccion.html', {'transaccion': transaccion})

# ============================================
# FUNCIONES PARA ACTUALIZACIONES (REDIRECCIONES)
# ============================================

def realizar_actualizacion_funcion(request, pk):
    return actualizar_funcion(request, pk)

def realizar_actualizacion_cliente(request, pk):
    return actualizar_cliente(request, pk)

def realizar_actualizacion_transaccion(request, pk):
    return actualizar_transaccion(request, pk)