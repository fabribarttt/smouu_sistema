from django.urls import path

from . import views

urlpatterns = [
    # ------------------------------ ATENCION AL CLIENTE ---------------------------------------------
    # Login, Panel principal, Logout
    path("", views.login_view, name="login"),
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
    # Generar nota de reparacion
    path("home/", views.home_view, name="home"),
    path("search_client/", views.search_client_view, name="search_clients"),
    path(
        "clients/<int:client_id>/select_device/",
        views.select_device_view,
        name="select_device",
    ),
    path("search_devices/<int:client_id>", views.search_devices, name="search_devices"),
    path(
        "clients/<int:client_id>/devices/<int:device_id>/create_repair/",
        views.create_repair_view,
        name="create_repair",
    ),
    path("repair_list/", views.read_repair_list_view, name="repair_list"),
    # ---------------------------------- SUPERVISOR -----------------------------------------------------
    path("panel_supervisor/", views.panel_supervisor_view, name="panel_supervisor"),
    # CRUD Inventario
    path("inventario/", views.inventario_view, name="inventario"),
    path("create_inventario/", views.create_inventario_view, name="create_inventario"),
    # CRUD Reportes
    path("reportes/", views.reportes_views, name="reportes"),
    # ---------------------------------- TECNICO --------------------------------------------------------
    path("panel_tecnico/", views.panel_tecnico_view, name="panel_tecnico"),
]
