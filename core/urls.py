from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

from .views import (
    registro_distribuidor,
    panel_distribuidor,
    agregar_precio,
    editar_precio,
)

urlpatterns = [
    # Página de inicio pública
    path('', views.home, name='home'),

    # Autenticación
    path('registro/', registro_distribuidor, name='registro'),
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),

    # Panel privado del distribuidor
    path('panel/', panel_distribuidor, name='panel_distribuidor'),
    path('panel/agregar/', agregar_precio, name='agregar_precio'),
    path('panel/editar/<int:pk>/', editar_precio, name='editar_precio'),
    path('como-funciona/', views.como_funciona, name='como_funciona'),

]
