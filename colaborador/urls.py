from django.urls import path
from colaborador.views import (login,
                               resgister,
                               # login_administrador,
                               painel_do_administrador,
                               # administradores,
                               colaboradores, editar_colaborador,
                               # editar_administrador, desmobilizar_administrador, administradores_desmobilizados,
                               # reabilitar_administrador,
                               desmobilizar_colaborador, colaboradores_desmobilizados,
                               reabilitar_colaborador, logout, insert_code)


urlpatterns = [
    # rota na raiz do sistema
    path('', login, name='login'),
    path('logout', logout, name='logout'),

    ##################################

    path('alterar-senha/', resgister, name='resgister'),
    # path('login-administrador', login_administrador, name='login_administrador'),

    path('confirm-update-password/', insert_code, name='insert_code'),

    ##################################

    path('painel-do-administrador/', painel_do_administrador, name='painel_do_administrador'),

    path('colaboradores/<str:login_type>/<int:id>', colaboradores, name='colaboradores'),
    path('colaboradores/editar/<str:login_type>/<int:colaborador_id>/<int:id>', editar_colaborador, name='editar_colaborador'),
    path('desmobilizar-colaborador/<str:login_type>/<int:colaborador_id>/<int:id>/<str:desm>', desmobilizar_colaborador, name='desmobilizar_colaborador'),
    path('colaboradores-desmobilizados/<str:login_type>/<int:id>', colaboradores_desmobilizados, name='colaboradores_desmobilizados'),
    path('reabilitar-colaborador/<str:login_type>/<int:colaborador_id>/<int:id>', reabilitar_colaborador, name='reabilitar_colaborador'),

    # path('administradores', administradores, name='administradores'),
    # path('editar_administrador/<int:administrador_id>', editar_administrador, name='editar_administrador'),
    # path('desmobilizar_administrador/<int:administrador_id>', desmobilizar_administrador, name='desmobilizar_administrador'),
    # path('administradores_desmobilizados', administradores_desmobilizados, name='administradores_desmobilizados'),
    # path('reabilitar_administrador/<int:administrador_id>', reabilitar_administrador, name='reabilitar_administrador')
]
