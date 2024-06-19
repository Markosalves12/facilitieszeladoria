from django.urls import path
from equipamento.views import (disponibilidade_equipamentos,
                               catalogo_de_equipamentos, editar_catalogo_de_equipamentos,
                               desmobilizar_equipamento_do_catalogo,
                               catalogo_de_equipamentos_desmobilizados, reabilitar_equipamento_do_catalogo,
                               equipamentos_disponiveis, editar_equipamento_disponivel,
                               equipamentos_desmobilizados, editar_equipamento_desmobilizado,
                               manutencao_de_equipamentos, cadastro_manutencao_equipamento,
                               historico_de_manutencao_equipamento, desmobilizar_equipamento_disponivel,
                               reabilitar_equipamento_desmobilizado, editar_manutencao_equipamento,
                               deletar_manutencao_do_historico_equipamento)


urlpatterns = [
    path('equipamentos/disponibilidade/', disponibilidade_equipamentos, name='disponibilidade_equipamentos'),

    path('equipamentos/catalogo/mobilizados/<str:login_type>/<int:id>', catalogo_de_equipamentos, name='catalogo_de_equipamentos'),
    path('equipamentos/catalogo/editar/<str:login_type>/<int:equipamento_catalogo_id>/<int:id>', editar_catalogo_de_equipamentos,
         name='editar_catalogo_de_equipamentos'),
    path('desmobilizar-equipamento-do-catalogo/<str:login_type>/<int:equipamento_catalogo_id>/<int:id>/<str:desm>',
         desmobilizar_equipamento_do_catalogo, name='desmobilizar_equipamento_do_catalogo'),
    path('equipamentos/catalogo/desmobilizados/<str:login_type>/<int:id>', catalogo_de_equipamentos_desmobilizados, name='catalogo_de_equipamentos_desmobilizados'),
    path('reabilitar-equipamento-do-catalogo/<str:login_type>/<int:equipamento_catalogo_id>/<int:id>', reabilitar_equipamento_do_catalogo, name='reabilitar_equipamento_do_catalogo'),

    path('equipamentos/mobilizados/<str:login_type>/<int:id>', equipamentos_disponiveis, name='equipamentos_disponiveis'),
    path('equipamentos/mobilizados/editar/<str:login_type>/<int:equipamento_disponivel_id>/<int:id>', editar_equipamento_disponivel,
         name='editar_equipamento_disponivel'),

    path('equipamentos/desmobilizados/<str:login_type>/<int:id>', equipamentos_desmobilizados, name='equipamentos_desmobilizados'),
    path('equipamentos/desmobilizados/editar/<str:login_type>/<int:equipamento_desmobilizado_id>/<int:id>', editar_equipamento_desmobilizado,
         name='editar_equipamento_desmobilizado'),

    path('equipamentos/manutencao/<str:login_type>/<int:id>', manutencao_de_equipamentos, name='manutencao_de_equipamentos'),
    path('equipamentos/manutencao/cadastro/<str:login_type>/<int:equipamento_disponivel_id>/<int:id>', cadastro_manutencao_equipamento,
         name='cadastro_manutencao_equipamento'),
    path('equipamentos/manutencao/cadastro/historico/<str:login_type>/<int:equipamento_disponivel_id>/<int:id>', historico_de_manutencao_equipamento,
         name='historico_de_manutencao_equipamento'),

    path('desmobilizar-equipamento-disponivel/<str:login_type>/<int:equipamento_disponivel_id>/<int:id>/<str:desm>',
         desmobilizar_equipamento_disponivel,
         name='desmobilizar_equipamento_disponivel'),

    path('reabilitar-equipamento-desmobilizado/<str:login_type>/<int:equipamento_desmobilizado_id>/<int:id>',
         reabilitar_equipamento_desmobilizado,
         name='reabilitar_equipamento_desmobilizado'),

    path('equipamentos/manutencao/editar/<str:login_type>/<int:manutencao_equipamento_id>/<int:id>',
         editar_manutencao_equipamento, name='editar_manutencao_equipamento'),

    path('equipamentos/manutencao/cadastro/historico/deletar/<str:login_type>/<int:manutencao_equipamento_id>/<int:id>',
         deletar_manutencao_do_historico_equipamento, name='deletar_manutencao_do_historico_equipamento')
]



