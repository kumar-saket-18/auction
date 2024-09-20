"""inventory URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from .views import add_player_to_team, dashboard, get_tc_cobras_list, get_tc_eagles_list, get_tc_hawks_list, history, generate_random_player, mark_unsold, generate_random_unsold_player

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', dashboard, name='dashboard'),
    path('users/', include('users.urls')),
    path('store/', include('store.urls')),
    path('add_player_to_team/', add_player_to_team, name='add_player_to_team'),
    path('get-tc-cobras-player-list/', get_tc_cobras_list, name='get-tc-cobras-player-list'),
    path('get-tc-eagles-player-list/', get_tc_eagles_list, name='get-tc-eagles-player-list'),
    path('get-tc-hawks-player-list/', get_tc_hawks_list, name='get-tc-hawks-player-list'),
    path('history/', history, name='history'),
    path('get-random-players/', generate_random_player, name='get-random-players'),
    path('get-unsold-random-players/', generate_random_unsold_player, name='get-unsold-random-players'),
    path('mark_unsold/', mark_unsold, name='mark_unsold'),

]
