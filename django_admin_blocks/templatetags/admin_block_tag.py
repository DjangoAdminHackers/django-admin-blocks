from django import template

register = template.Library()

@register.inclusion_tag('admin_error_blocks.html', takes_context=True)
def error_blocks(context):
    from django_admin_blocks import _error_registry
    blocks = [x for x in [x() for x in _error_registry] if x]
    return {
        'blocks': blocks,
    }

@register.simple_tag(takes_context=True)
def app_block(context, app):
    from django_admin_blocks import _app_block_registry
    html = u''
    for tuple in _app_block_registry:
        if tuple[0].lower()==app['name'].lower():
            # TODO move this into a template to allow overriding
            html += u'\n'.join(["<tr><th scope='row' colspan='3'>%s</th></tr>" % x() for x in tuple[1:]])
    return html

@register.simple_tag
def script_block():
    from django_admin_blocks import _script_block_registry
    html = u''
    for script in _script_block_registry:
        html += u'%s\n' % script
    return html
