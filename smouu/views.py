from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegisterClientForm, CreateDispositivoForm
from .models import Cliente, Dispositivo


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Bienvenido")
            return redirect("home")
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


def home_view(request):
    return render(request, "home.html")


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
