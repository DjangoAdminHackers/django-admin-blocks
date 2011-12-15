from django import template

register = template.Library()

# TODO auto-register these permissions somewhere. Currently this will hide all notifications for non-superusers
# TODO add per app and per notification permissions

@register.inclusion_tag('admin_error_notifications.html', takes_context=True)
def error_notifications(context):
    if context['request'].user.has_perm('admin_notifications.can_see_error_notifications'):
        from admin_notifications import _error_registry
        notifications = [x for x in [x() for x in _error_registry] if x]
    else:
        notifications = []
    return {
        'notifications': notifications,
    }

@register.simple_tag(takes_context=True)
def app_block(context, app):
    if context['request'].user.has_perm('admin_notifications.can_see_app_blocks'):
        from admin_notifications import _app_block_registry
        html = u''
        for tuple in _app_block_registry:
            if tuple[0].lower()==app['name'].lower():
                html += u'\n'.join(["<tr><th scope='row' colspan='3'>%s</th></tr>" % x() for x in tuple[1:]])
    else:
        html = ''
    return html

@register.simple_tag
def extra_script_block():
    from admin_notifications import _script_block_reqistry
    html = u''
    for script in _script_block_reqistry:
        html += u'%s\n' % script()
    return html
