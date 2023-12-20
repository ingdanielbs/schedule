from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter
def replace(value, args):
    search, replace_with = args.split(',')
    return value.replace(search, replace_with)