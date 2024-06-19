from django.urls import path
from gerente.views import (gerentes, editar_gerente,
                           gerentes_desmobilizados, desmobilizar_gerente, reabilitar_gerente)


urlpatterns = [
    path('gerentes/mobilizados/<str:login_type>/<int:id>', gerentes, name='gerentes'),
    path('gerentes/editar/<str:login_type>/<int:gerente_id>/<int:id>', editar_gerente, name='editar_gerente'),
    path('gerentes/desmobilizados/<str:login_type>/<int:id>', gerentes_desmobilizados, name='gerentes_desmobilizados'),
    path('desmobilizar-gerente/<str:login_type>/<int:gerente_id>/<int:id>/<str:desm>', desmobilizar_gerente, name='desmobilizar_gerente'),
    path('reabilitar-gerente/<str:login_type>/<int:gerente_id>/<int:id>', reabilitar_gerente, name='reabilitar_gerente'),
]