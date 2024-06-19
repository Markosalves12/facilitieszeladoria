from django.urls import path
from dashboards.views import (relatoriodeservicos, exportar_excel,
                              relatoriopdf, exportar_pdf,
                              relatoriomanutencaoequipamentos,
                              exportar_relatorio_manutencao_equipamentos,
                              relatoriomanutencaoferramentas,
                              exportar_relatorio_manutencao_ferramentas)


urlpatterns = [
    path('relatorio-de-servicos/', relatoriodeservicos,
         name='relatoriodeservicos'),
    path('exportar-excel/<str:login_type>/<int:id>/<str:datastart>/'
         '<str:datafim>/<str:empresa>/<str:unidade>/<str:localidades>/<str:negocios>',
         exportar_excel, name='exportar_excel'),

    path('relatorio-pdf/', relatoriopdf,
         name='relatoriopdf'),
    path('exportar_pdf/<str:login_type>/<int:id>/<str:datastart>/'
         '<str:datafim>/<str:empresa>/<str:unidade>/<str:localidades>/<str:negocios>/<str:carteira>',
         exportar_pdf,
         name='exportar_pdf'),

    path('relatorio-manutencao-de-equipamentos/', relatoriomanutencaoequipamentos,
         name='relatoriomanutencaoequipamentos'),
    path('exportar-relatorio-manutencao-equipamentos/<str:login_type>/<int:id>/<str:datastart>/<str:datafim>/<str:unidades>/<str:empresas>/<str:tipomanutencao>/',
         exportar_relatorio_manutencao_equipamentos, name='exportar_relatorio_manutencao_equipamentos'),

    path('relatorio-manutencao-de-ferramentas/', relatoriomanutencaoferramentas,
         name='relatoriomanutencaoferramentas'),
    path('exportar-relatorio-manutencao-ferramentas/<str:login_type>/<int:id>/<str:datastart>/<str:datafim>/<str:unidades>/<str:empresas>/<str:tipomanutencao>/',
         exportar_relatorio_manutencao_ferramentas, name='exportar_relatorio_manutencao_ferramentas'),
]