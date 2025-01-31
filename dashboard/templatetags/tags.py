from django import template

register = template.Library()

@register.filter
def get_attr(obj, attr):
    """Get an attribute from an object dynamically."""
    return getattr(obj, attr, None)