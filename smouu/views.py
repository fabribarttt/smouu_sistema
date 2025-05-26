from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .forms import (
    RegisterClientForm,
    CreateDispositivoForm,
    SearchClientForm,
    SearchDeviceForm,
    RepairTicketForm,
    RegistrarRepuesto,
)
from .models import (
    Cliente,
    Dispositivo,
    OrdenReparacion,
    InventarioRepuesto,
    Empleado,
    AsignacionReparacion,
)


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Bienvenido")
            # De acuerdo al rol del usuario sera redirigido a su respectivo panel
            if user.groups.filter(name="atencion al cliente").exists():
                return redirect("home")
            elif user.groups.filter(name="supervisor").exists():
                return redirect("panel_supervisor")
            elif user.groups.filter(name="tecnico").exists():
                return redirect("panel_tecnico")
            else:
                return redirect("login")
            # ----------------------------------------------------------------------
        else:
            messages.warning(request, "Usuario o contraseña incorrecto")
            return redirect("login")
    elif request.user.is_authenticated:
        return redirect("logout")
    else:
        return render(request, "login.html")


def logout_view(request):
    logout(request)
    messages.success(request, "Ha cerrado sesion")
    return redirect("login")


# -------------------------------- PANEL ATENCION AL CLIENTE --------------------------------------
# GENERAR ORDEN DE REPARACION
@login_required
def home_view(request):
    form = SearchClientForm()
    return render(request, "repairs/client_search.html", {"form": form})


@login_required
def search_client_view(request):
    search_term = request.GET.get("search_term", "")

    if search_term:
        clients = Cliente.objects.filter(Q(cedula__icontains=search_term))
    else:
        clients = Cliente.objects.none()

    return render(request, "repairs/client_list_partial.html", {"clients": clients})


@login_required
def select_device_view(request, client_id):
    client = Cliente.objects.get(id=client_id)
    form = SearchDeviceForm()

    return render(
        request,
        "repairs/device_selection.html",
        {"client": client, "client_id": client_id, "form": form},
    )


@login_required
def search_devices(request, client_id):
    search_term = request.GET.get("search_term", "")

    if search_term:
        devices = Dispositivo.objects.filter(
            Q(marca__icontains=search_term) | Q(modelo__icontains=search_term)
        )
    else:
        devices = Dispositivo.objects.none()

    return render(
        request,
        "repairs/device_list_partial.html",
        {"devices": devices, "client_id": client_id},
    )


@login_required
def create_repair_view(request, client_id, device_id):
    client = Cliente.objects.get(id=client_id)
    device = Dispositivo.objects.get(id=device_id)
    empleado = Empleado.objects.get(usuario=request.user)

    if request.method == "POST":
        form = RepairTicketForm(request.POST)
        if form.is_valid():
            repair = form.save(commit=False)
            repair.id_cliente = client
            repair.id_dispositivo = device
            repair.id_empleado = empleado
            repair.save()
            return redirect("repair_list")
    else:
        form = RepairTicketForm()

    return render(
        request,
        "repairs/repair_form.html",
        {
            "form": form,
            "client": client,
            "device": device,
        },
    )


@login_required
def read_repair_list_view(request):
    reparaciones = OrdenReparacion.objects.select_related(
        "id_cliente", "id_dispositivo"
    ).prefetch_related("asignacionreparacion_set")
    return render(request, "repairs/repair_list.html", {"reparaciones": reparaciones})


# CRUD CLIENTES
# Funcion para registrar los clientes renderiza el html y recibe un POST con los datos ingresados en el formulario y lo guarda en la base de datos
def create_client_view(request):
    if request.user.is_authenticated:
        form = RegisterClientForm(request.POST or None)
        if request.method == "POST":
            if form.is_valid():
                form.save()
                messages.success(request, "El cliente se ha registrado correctamente")
                return redirect("read_client")
        else:
            return render(request, "clients/create_client.html", {"form": form})
    else:
        messages.error(request, "Debes de iniciar sesion")
        return redirect("login")


# Funcion para visualizar los clientes ya registrados y renderiza el HTML
def read_client_view(request):
    if request.user.is_authenticated:
        clientes = Cliente.objects.all
        return render(request, "clients/read_client.html", {"clientes": clientes})
    else:
        messages.error(request, "Debes de iniciar sesion")
        return redirect("login")


def update_client_view(request, pk):
    if request.user.is_authenticated:
        current_client = Cliente.objects.get(id=pk)
        form = RegisterClientForm(request.POST or None, instance=current_client)
        if form.is_valid():
            form.save()
            messages.success(request, "Los datos del cliente se actualizaron")
            return redirect("read_client")
        return render(request, "clients/update_client.html", {"form": form})
    else:
        messages.error(request, "Debes de iniciar sesion")
        return redirect("login")


def delete_client_view(request, pk):
    if request.user.is_authenticated:
        delete_it = Cliente.objects.get(id=pk)
        delete_it.delete()
        messages.success(request, "Se ha eliminado correctamente")
        return redirect("read_client")
    else:
        messages.error(request, "Debes iniciar sesion")
        return redirect("login")


# CRUD Dispositivos
@login_required
def create_device_view(request):
    form = CreateDispositivoForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, "Se ha registrado el dispositivo")
            return redirect("read_device")
    else:
        return render(request, "devices/create_device.html", {"form": form})


@login_required
def read_device_view(request):
    dispositivo = Dispositivo.objects.all()
    return render(request, "devices/read_device.html", {"dispositivos": dispositivo})


@login_required
def update_device_view(request, pk):
    current_device = Dispositivo.objects.get(id=pk)
    form = CreateDispositivoForm(request.POST or None, instance=current_device)
    if form.is_valid():
        form.save()
        messages.success(request, "Se actualizo los datos del dispositivo")
        return redirect("read_device")
    else:
        return render(request, "devices/update_device.html", {"form": form})


@login_required
def delete_device_view(request, pk):
    delete_it = Dispositivo.objects.get(id=pk)
    delete_it.delete()
    messages.success(request, "El dispositivo se ha eliminado")
    return redirect("read_device")


# --------------------------------- PANEL SUPERVISOR -----------------------------------------


@login_required
# Vista de las ordenes de reparacion para asignar a un tecnico
def panel_supervisor_view(request):
    ordenes = OrdenReparacion.objects.filter(asignacionreparacion__isnull=True)
    tecnicos = Empleado.objects.filter(rol__name="tecnico")

    if request.method == "POST":
        orden_id = request.POST.get("orden_id")
        tecnico_id = request.POST.get("tecnico_id")

        if orden_id and tecnico_id:
            orden = OrdenReparacion.objects.get(id=orden_id)
            tecnico = Empleado.objects.get(id=tecnico_id)

            AsignacionReparacion.objects.create(
                id_orden=orden,
                id_empleado=tecnico,
                estado_reparacion="pendiente",  # o el estado inicial que quieras
            )

            messages.success(request, "Técnico asignado correctamente")
        else:
            messages.warning(request, "Porfavor seleccione un tecnico")

    return render(
        request,
        "panel_supervisor/asignacion_reparacion/lista_ordenes_reparacion.html",
        {
            "ordenes": ordenes,
            "tecnicos": tecnicos,
        },
    )


# CRUD Inventario
def inventario_view(request):
    inventario = InventarioRepuesto.objects.select_related(
        "id_categoria", "id_proveedor"
    ).all()
    return render(
        request, "panel_supervisor/inventario.html", {"inventario": inventario}
    )


def create_inventario_view(request):
    form = RegistrarRepuesto(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, "Se ha registrado el repuesto")
            return redirect("inventario")
    else:
        return render(
            request, "panel_supervisor/create_inventario.html", {"form": form}
        )


def reportes_views(request):
    return render(request, "panel_supervisor/reportes.html")


# --------------------------------- PANEL TECNICO ---------------------------------------------
@login_required
def panel_tecnico_view(request):
    tecnico = request.user.empleado
    asignaciones = AsignacionReparacion.objects.select_related(
        "id_orden", "id_orden__id_dispositivo"
    ).filter(id_empleado=tecnico)
    return render(request, "panel_tecnico/home.html", {"asignaciones": asignaciones})
