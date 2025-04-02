from django import template

register = template.Library()

@register.filter
def get_attr(obj, attr):
    """Get an attribute from an object dynamically."""
    return getattr(obj, attr, None)


@register.filter
def prepend_hyphen(value):
    """Prepend a hyphen to each line of the input text."""
    if not value:
        return value
    return '\n'.join(f'- {line}' for line in value.splitlines())