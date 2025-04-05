from django.urls import path
from . import views

urlpatterns = [
    # Login, Panel principal, Logout
    path("", views.login_view, name="login"),
    path("home/", views.home_view, name="home"),
    path("logout/", views.logout_view, name="logout"),
    # CRUD Clientes
    path("create_client/", views.create_client_view, name="create_client"),
    path("read_client/", views.read_client_view, name="read_client"),
    path("update_client/<int:pk>", views.update_client_view, name="update_client"),
    path("delete_client/<int:pk>", views.delete_client_view, name="delete_client"),
    # CRUD Dispositivos
    path("create_device/", views.create_device_view, name="create_device"),
    path("read_device/", views.read_device_view, name="read_device"),
    path("update_device/<int:pk>", views.update_device_view, name="update_device"),
    path("delete_device/<int:pk>", views.delete_device_view, name="delete_device"),
]
