from django.template.defaulttags import register

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter
def meal(query, meal):
    return query.filter(meal=meal)