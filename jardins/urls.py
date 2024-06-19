from django.urls import path
from jardins.views import (areas_verdes, areas, editar_area, desmobilizar_area, areas_desmobilizadas,
                           reabilitar_area)


urlpatterns = [
    path('areas-verdes/<str:unidade>/<path:link>/', areas_verdes, name='areas_verdes'),
    path('areas-verdes/mobilizadas/<str:login_type>/<int:id>', areas, name='areas'),
    path('areas_verdes/editar/<str:login_type>/<int:area_id>/<int:id>', editar_area, name='editar_area'),
    path('desmobilizar-area/<str:login_type>/<int:area_id>/<int:id>/<str:desm>', desmobilizar_area, name='desmobilizar_area'),
    path('areas-verdes/desmobilizadas/<str:login_type>/<int:id>', areas_desmobilizadas, name='areas_desmobilizadas'),
    path('reabilitar-area/<str:login_type>/<int:area_id>/<int:id>', reabilitar_area, name='reabilitar_area'),
]
