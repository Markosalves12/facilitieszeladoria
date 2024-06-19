from django.urls import path
from gestor.views import (gestores, editar_gestor, gestores_desmobilizados,
                          desmobilizar_gestor, reabilitar_gestor)


urlpatterns = [
    path('gestores/mobilizados/<str:login_type>/<int:id>', gestores, name='gestores'),
    path('gestores/editar/<str:login_type>/<int:gestor_id>/<int:id>', editar_gestor, name='editar_gestor'),
    path('desmobilizar-gestor/<str:login_type>/<int:gestor_id>/<int:id>', desmobilizar_gestor, name='desmobilizar_gestor'),
    path('gestores/desmobilizados/<str:login_type>/<int:id>', gestores_desmobilizados, name='gestores_desmobilizados'),
    path('reabilitar-gestor/<str:login_type>/<int:gestor_id>/<int:id>', reabilitar_gestor, name='reabilitar_gestor'),
]