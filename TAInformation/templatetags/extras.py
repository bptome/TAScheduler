from django.template.defaulttags import register


@register.filter(name='zip')
def zip_lists(a, b):
    return zip(a, b)
