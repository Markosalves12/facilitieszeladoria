from unidadee.models import Unidade

# retorna as unidades para o menu lateral
def unidades_info(request):
    unidade_info = Unidade.objects.exclude(status='Desmobilizado')

    return {
        'unidade_info': unidade_info,
    }
