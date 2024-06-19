from django.urls import path
from empresa.views import (empresas, editar_empresa,
                           desmobilizar_empresa, empresas_desmobilizadas, reabilitar_empresa)


urlpatterns = [
    # listagem das empresas
    path('empresas/<str:login_type>/<int:id>', empresas, name='empresas'),
    # editar empresa
    path('empresas/editar/<str:login_type>/<int:empresa_id>/<int:id>', editar_empresa, name='editar_empresa'),
    # desmobilizar empresa
    # alterar status
    path('desmobilizar-empresa/<str:login_type>/<int:empresa_id>/<int:id>/<str:desm>', desmobilizar_empresa, name='desmobilizar_empresa'),
    # listagem, de empresas desmobilizadas
    path('empresas-desmobilizadas/<str:login_type>/<int:id>', empresas_desmobilizadas, name='empresas_desmobilizadas'),
    # mobilizar empresa
    # alterar empresa
    path('reabilitar-empresa/<str:login_type>/<int:empresa_id>/<int:id>', reabilitar_empresa, name='reabilitar_empresa'),
]