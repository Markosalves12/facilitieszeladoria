from django.urls import path
from manutencao.views import (catalogo_de_manutencao, editar_manutencao,
                              desmobilizar_manutencao, manutencoes_desmobilizadas,
                              reabilitar_manutencao)

urlpatterns = [
    path('catalogo_de_manutencao/<str:login_type>/<int:id>', catalogo_de_manutencao, name='catalogo_de_manutencao'),
    path('editar_manutencao/<str:login_type>/<int:manutencao_id>/<int:id>', editar_manutencao,
         name='editar_manutencao'),
    path('desmobilizar_manutencao/<str:login_type>/<int:manutencao_id>/<int:id>/<str:desm>', desmobilizar_manutencao,
         name='desmobilizar_manutencao'),
    path('manutencoes_desmobilizadas/<str:login_type>/<int:id>', manutencoes_desmobilizadas, name='manutencoes_desmobilizadas'),
    path('reabilitar_manutencao/<str:login_type>/<int:manutencao_id>/<int:id>', reabilitar_manutencao,
         name='reabilitar_manutencao'),
]