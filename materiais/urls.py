from django.urls import path
from materiais.views import (materiais, editar_material, desmobilizar_material,
                             materiais_desmobilizados, reabilitar_material)


urlpatterns = [
    path('materiais/mobilizados/<str:login_type>/<int:id>', materiais, name='materiais'),
    path('materiais/editar/<str:login_type>/<int:material_id>/<int:id>', editar_material,
         name='editar_material'),
    path('materiais-desmobilizar/<str:login_type>/<int:material_id>/<int:id>/<str:desm>', desmobilizar_material,
         name='desmobilizar_material'),
    path('materiais/desmobilizados/<str:login_type>/<int:id>', materiais_desmobilizados,
         name='materiais_desmobilizados'),
    path('reabilitar-material/<str:login_type>/<int:material_id>/<int:id>',
         reabilitar_material, name='reabilitar_material'),
]