from django import template

register = template.Library()

@register.filter
def key_in_dict(dictionary, key):
    """
    Verifica se a chave existe em um dicionário.
    Útil para chaves que são tuplas em templates.
    """
    return key in dictionary

from django import template

register = template.Library()

@register.filter
def key_in_dict(dictionary, key):
    """
    Verifica se a chave existe em um dicionário.
    Útil para chaves que são tuplas em templates.
    """
    return key in dictionary

@register.filter
def range(value):
    """
    Gera uma lista de números de 0 a (value-1).
    Uso: {% for i in 5|range %}
    """
    return [i for i in range(value)]