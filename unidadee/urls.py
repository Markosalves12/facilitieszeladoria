from django.urls import path
from unidadee.views import (unidades, editar_unidade,
                            localidades, editar_localidade, desmobilizar_localidade,
                            desmobilizar_unidade, unidades_desmobilizadas, reabilitar_unidade,
                            localidades_desmobilizadas, reabilitar_localidade)


urlpatterns = [
    path('unidades/mobilizados/<str:login_type>/<int:id>', unidades, name='unidades'),
    path('unidades/editar/<str:login_type>/<int:unidade_id>/<int:id>', editar_unidade, name='editar_unidade'),
    path('desmobilizar-unidade/<str:login_type>/<int:unidade_id>/<int:id>', desmobilizar_unidade, name='desmobilizar_unidade'),
    path('unidades/desmobilizadas/<str:login_type>/<int:id>', unidades_desmobilizadas, name='unidades_desmobilizadas'),
    path('reabilitar_unidade/<str:login_type>/<int:unidade_id>/<int:id>', reabilitar_unidade, name='reabilitar_unidade'),

    path('localidades/mobilizados/<str:login_type>/<int:id>', localidades, name='localidades'),
    path('localidades/editar/<str:login_type>/<int:localidade_id>/<int:id>', editar_localidade, name='editar_localidade'),
    path('desmobilizar-localidade/<str:login_type>/<int:localidade_id>/<int:id>/<str:desm>', desmobilizar_localidade, name='desmobilizar_localidade'),
    path('localidades/desmobilizadas/<str:login_type>/<int:id>', localidades_desmobilizadas, name='localidades_desmobilizadas'),
    path('reabilitar-localidade/<str:login_type>/<int:localidade_id>/<int:id>', reabilitar_localidade, name='reabilitar_localidade'),
]