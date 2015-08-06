import imp

_error_registry = []
_alert_registry = []
_app_block_registry = []
_script_block_registry = []


def register(blocks):
    
    for ntype in blocks.keys():
        registry = {
            'errors': _error_registry,
            'app_blocks': _app_block_registry,
            'script_blocks': _script_block_registry,
        }[ntype]
        registry += [x for x in blocks[ntype] if x]


def autodiscover():
    
    from django.conf import settings
    for app in settings.INSTALLED_APPS:
        try:
            app_path = __import__(app, {}, {}, [app.split('.')[-1]]).__path__
        except AttributeError:
            continue
        try:
            imp.find_module('admin_blocks', app_path)
        except ImportError:
            continue
        __import__("%s.admin_blocks" % app)


