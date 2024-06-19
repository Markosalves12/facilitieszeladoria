from django.urls import path
from ferramenta.views import (disponibilidade_ferramentas,
                              catalogo_de_ferramentas, editar_catalogo_de_ferramentas,
                              ferramentas_disponiveis, editar_ferramenta_disponivel,
                              desmobilizar_ferramenta_do_catalogo, catalogo_de_ferramentas_desmobilizadas,
                              ferramentas_desmobilizadas, editar_ferramenta_desmobilizada, reabilitar_ferramenta_do_catalogo,
                              manutencao_de_ferramentas, cadastro_manutencao_ferramenta,
                              historico_de_manutencao_ferramenta, desmobilizar_ferramenta_disponivel,
                              reabilitar_ferramenta_desmobilizado, editar_manutencao_ferramenta,
                              deletar_manutencao_do_historico)


urlpatterns = [
    path('ferramentas/disponibilidade/', disponibilidade_ferramentas, name='disponibilidade_ferramentas'),

    path('ferramentas/catalogo/mobilidos/<str:login_type>/<int:id>', catalogo_de_ferramentas, name='catalogo_de_ferramentas'),
    path('ferramentas/catalogo/editar/<str:login_type>/<int:ferramenta_catalogo_id>/<int:id>', editar_catalogo_de_ferramentas,
         name='editar_catalogo_de_ferramentas'),

    path('desmobilizar-ferramenta-do-catalogo/<str:login_type>/<int:ferramenta_catalogo_id>/<int:id>/<str:desm>',
         desmobilizar_ferramenta_do_catalogo, name='desmobilizar_ferramenta_do_catalogo'),
    path('ferramentas/catalogo/desmobilizados/<str:login_type>/<int:id>', catalogo_de_ferramentas_desmobilizadas, name='catalogo_de_ferramentas_desmobilizadas'),
    path('reabilitar-ferramenta-do-catalogo/<str:login_type>/<int:ferramenta_catalogo_id>/<int:id>', reabilitar_ferramenta_do_catalogo, name='reabilitar_ferramenta_do_catalogo'),


    path('ferramentas/mobilizados/<str:login_type>/<int:id>', ferramentas_disponiveis, name='ferramentas_disponiveis'),
    path('ferramentas/mobilizados/editar/<str:login_type>/<int:ferramenta_disponivel_id>/<int:id>', editar_ferramenta_disponivel,
         name='editar_ferramenta_disponivel'),


    path('ferramentas/desmobilizados/<str:login_type>/<int:id>', ferramentas_desmobilizadas, name='ferramentas_desmobilizadas'),
    path('ferramentas/desmobilizados/editar/<str:login_type>/<int:ferramenta_desmobilizado_id>/<int:id>', editar_ferramenta_desmobilizada,
         name='editar_ferramenta_desmobilizada'),


    path('ferramentas/manutencao/<str:login_type>/<int:id>', manutencao_de_ferramentas, name='manutencao_de_ferramentas'),
    path('ferramentas/manutencao/cadastro/<str:login_type>/<int:ferramenta_disponivel_id>/<int:id>', cadastro_manutencao_ferramenta,
         name='cadastro_manutencao_ferramenta'),
    path('ferramentas/manutencao/historico/<str:login_type>/<int:ferramenta_disponivel_id>/<int:id>', historico_de_manutencao_ferramenta,
         name='historico_de_manutencao_ferramenta'),

    path('desmobilizar-ferramenta-disponivel/<str:login_type>/<int:ferramenta_disponivel_id>/<int:id>/<str:desm>',
         desmobilizar_ferramenta_disponivel,
         name='desmobilizar_ferramenta_disponivel'),

    path('reabilitar-ferramenta-desmobilizado/<str:login_type>/<int:ferramenta_desmobilizado_id>/<int:id>',
         reabilitar_ferramenta_desmobilizado,
         name='reabilitar_ferramenta_desmobilizado'),

    path('ferramentas/manutencao/editar/<str:login_type>/<int:manutencao_ferramenta_id>/<int:id>',
         editar_manutencao_ferramenta, name='editar_manutencao_ferramenta'),

    path('ferramentas/manutencao/deletar/<str:login_type>/<int:manutencao_ferramenta_id>/<int:id>',
         deletar_manutencao_do_historico, name='deletar_manutencao_do_historico')
]
