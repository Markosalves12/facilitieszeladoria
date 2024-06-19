from django.urls import path
from servico.views import (servicos_concluidos,
                           servicos_agendados, iniciar_servico,
                           catalogo_de_servicos, editar_catalogo_de_servicos,desmobilizar_servico_do_catalogo,
                           catalogo_de_servicos_desmobilizados, reabilitar_servico_do_catalogo,
                           servicos, editar_servico_agendado, cancelar_servico_agendado,
                           solicitar_servico, execucao_de_servicos,
                           executar_servico, concluir_servico)

urlpatterns = [
    path('servicos/concluidos/<str:login_type>/<int:id>', servicos_concluidos, name='servicos_concluidos'),
    path('servicos/agendados/<str:login_type>/<int:id>', servicos_agendados, name='servicos_agendados'),
    path('servicos/iniciar/<int:servico_id>/<str:login_type>/<int:id>', iniciar_servico, name='iniciar_servico'),


    path('servicos/catalogo/mobilizados/<str:login_type>/<int:id>', catalogo_de_servicos, name='catalogo_de_servicos'),
    path('servicos/catalogo/editar/<str:login_type>/<int:servico_catalogo_id>/<int:id>', editar_catalogo_de_servicos,
         name='editar_catalogo_de_servicos'),
    path('desmobilizar-servico-do-catalogo/<str:login_type>/<int:servico_catalogo_id>/<int:id>/<str:desm>', desmobilizar_servico_do_catalogo,
         name='desmobilizar_servico_do_catalogo'),
    path('servicos/catalogo/desmobilizados/<str:login_type>/<int:id>', catalogo_de_servicos_desmobilizados, name='catalogo_de_servicos_desmobilizados'),
    path('reabilitar-servico-do-catalogo/<str:login_type>/<int:servico_catalogo_id>/<int:id>', reabilitar_servico_do_catalogo, name='reabilitar_servico_do_catalogo'),



    path('servicos/status=agendado&status=emandamento/<str:login_type>/<int:id>', servicos, name='servicos'),
    path('servicos/status=agendado&status=emandamento/editar/<str:login_type>/<int:servico_id>/<int:id>', editar_servico_agendado,
         name='editar_servico_agendado'),
    path('cancelar-servico-agendado/<str:login_type>/<int:servico_id>/<int:id>', cancelar_servico_agendado,
         name='cancelar_servico_agendado'),
    path('servicos/solicitar/<str:login_type>/<int:id>',solicitar_servico, name='solicitar_servico'),
    path('servicos/prestacao/<str:login_type>/<int:id>', execucao_de_servicos, name='execucao_de_servicos'),
    path('servicos/executar/<str:login_type>/<int:id>', executar_servico, name='executar_servico'),
    path('concluir-servico/<int:servico_id>/<str:login_type>/<int:id>', concluir_servico, name='concluir_servico'),
]