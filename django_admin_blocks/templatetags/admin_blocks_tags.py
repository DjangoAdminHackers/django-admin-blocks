from django import template
from django.conf import settings

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

@register.simple_tag(takes_context=True)
def script_block(context):

    from django_admin_blocks import _script_block_registry

    # Remove dups while preserving order
    already_seen = set()
    new_list = []
    for d in _script_block_registry:
        t = tuple(d.items())
        if t not in already_seen:
            already_seen.add(t)
            new_list.append(d)
    _script_block_registry = new_list

    scripts = [
        # Use Django's jQuery if nothing else is available
        u'<script>if(typeof($) === "undefined" && typeof(django.jQuery) != "undefined"){var $ = django.jQuery; var jQuery = $;}</script>',
    ]

    for script in _script_block_registry:
        if script.get('url_path'):
            scripts.append(u'<script src="%s%s"></script>' % (settings.STATIC_URL, script['url_path']))
        elif script.get('code'):
            scripts.append(u'<script>\n%s</script>' % script['code'])

    return '\n'.join(scripts)
