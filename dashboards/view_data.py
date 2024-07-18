from django.db.models import Sum, Count
import plotly.graph_objs as go
from django.db.models.functions import TruncMonth
from plotly.offline import plot
import calendar
from django.db.models import F

def get_total_area_by_category(queryset, category_field):
    """
    Calcula a soma das áreas e as contagens de itens para cada categoria.

    Args:
        queryset: A consulta do Django ORM.
        category_field: O campo da categoria a ser agrupado.

    Returns:
        Um dicionário com a categoria como chave e a soma das áreas como valor.
        Um dicionário com a categoria como chave e a contagem de itens como valor.
    """
    data = queryset.values(category_field).annotate(
        total_area=Sum('area__area'),
        count=Count('id')
    ).order_by()

    total_area_by_category = {item[category_field]: item['total_area'] for item in data}
    counts_by_category = {item[category_field]: item['count'] for item in data}

    return total_area_by_category, counts_by_category


def plot_horizontal_bar_chart(data, title, x_axis_title, y_axis_title, counts, marker_color='#000080'):
    """
    Gera um gráfico de barras horizontais.

    Args:
        data: Um dicionário com a categoria como chave e a soma das áreas como valor.
        title: O título do gráfico.
        x_axis_title: O título do eixo x.
        y_axis_title: O título do eixo y.

    Returns:
        Uma figura Plotly do gráfico de barras horizontais.
    """
    categories = list(data.keys())
    values = list(data.values())
    hovertexts = [f'Área Total: {v}<br>Servicos: {counts[c]}' for c, v in data.items()]


    # Calcula a altura dinamicamente com base no número de categorias
    base_height = 300  # Altura base mínima
    extra_height_per_category = 20  # Altura adicional por categoria
    height = base_height + extra_height_per_category * len(categories)

    fig = go.Figure(go.Bar(
        x=values,
        y=categories,
        orientation='h',
        marker_color=marker_color,
        width=0.3,
        text=hovertexts,
        textposition='auto',
        hovertext=hovertexts,
        hoverinfo='text'
    ))

    fig.update_layout(
        title=title,
        xaxis_title=x_axis_title,
        yaxis_title=y_axis_title,
        margin=dict(l=0, r=0, t=27, b=0),  # Ajustando as margens
        bargap=0.1,
        height=height
    )

    return fig


def get_total_area_and_counts_by_month(queryset, field_name):
    """
    Calcula a soma das áreas e as contagens de itens para cada mês e campo especificado.

    Args:
        queryset: A consulta do Django ORM.
        field_name: O nome do campo para agrupamento (e.g., 'area__vegetacao', 'area__terreno').

    Returns:
        Um dicionário com o mês como chave e a soma das áreas como valor.
        Um dicionário com o mês como chave e a contagem de itens como valor.
        Um dicionário com o mês como chave e a categoria como valor.
    """
    data = queryset.annotate(
        month=TruncMonth('data_inicio'),
        category=F(field_name)
    ).values('month', 'category').annotate(
        total_area=Sum('area__area'),
        count=Count('id')
    ).order_by('month', 'category')

    total_area_by_month = {}
    counts_by_month = {}
    categories_by_month = {}

    for item in data:
        month = item['month']
        category = item['category']
        month_str = f"{calendar.month_abbr[month.month]}/{month.year}"

        if month_str not in total_area_by_month:
            total_area_by_month[month_str] = {}
            counts_by_month[month_str] = {}
            categories_by_month[month_str] = {}

        total_area_by_month[month_str][category] = item['total_area']
        counts_by_month[month_str][category] = item['count']
        categories_by_month[month_str][category] = category

    return total_area_by_month, counts_by_month, categories_by_month


def plot_grouped_bar_chart(data, title, x_axis_title, y_axis_title, counts, categories, label_type, marker_colors=None):
    """
    Gera um gráfico de barras agrupadas.

    Args:
        data: Um dicionário aninhado com meses como chaves externas e categorias como chaves internas,
              e a soma das áreas como valores internos.
        title: O título do gráfico.
        x_axis_title: O título do eixo x.
        y_axis_title: O título do eixo y.
        counts: Um dicionário aninhado com meses como chaves externas e categorias como chaves internas,
                e a contagem de itens como valores internos.
        categories: Um dicionário aninhado com meses como chaves externas e categorias como chaves internas,
                    e o nome da categoria como valores internos.
        label_type: Uma string que especifica se é 'vegetação' ou 'terreno'.
        marker_colors: Lista de cores das barras.

    Returns:
        Uma string HTML contendo a figura Plotly do gráfico de barras agrupadas.
    """
    fig = go.Figure()

    months = list(data.keys())
    categories_list = list({cat for month in data.values() for cat in month.keys()})

    for i, category in enumerate(categories_list):
        values = [data[month].get(category, 0) for month in months]
        hovertexts = [
            f'{label_type.capitalize()}: {categories[month].get(category, "N/A")}<br>Mês: {month}<br>Área Total: {data[month].get(category, 0)}<br>Serviços: {counts[month].get(category, 0)}'
            for month in months
        ]

        fig.add_trace(go.Bar(
            x=months,
            y=values,
            name=category,
            marker_color=marker_colors[i] if marker_colors else None,
            text=hovertexts,
            textposition='auto',
            hovertext=hovertexts,
            hoverinfo='text'
        ))

    fig.update_layout(
        title=title,
        xaxis_title=x_axis_title,
        yaxis_title=y_axis_title,
        barmode='group',
        margin=dict(l=0, r=0, t=27, b=0),  # Ajustando as margens
        height=300
    )

    return fig