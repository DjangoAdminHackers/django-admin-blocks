from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=Permission)
def create_app_permissions(sender, **kwargs):
    """Creates permissions for the admin_notifications app which aren't tied
    to models (because the app doesn't have any).
    
    This will be run after the Permission model is saved so running syncdb
    without an auth_permission table creates these permissions.
    """
    # Create a content type for the app if it doesn't already exist
    ct, created = ContentType.objects.get_or_create(model='',
                                                    app_label='admin_notifications',
                                                    defaults={'name': 'admin notifications'})

    # Create permissions if they don't already exist
    Permission.objects.get_or_create(codename='can_see_error_notifications',
                                     content_type__pk=ct.id,
                                     defaults={'name': 'Can see error notifications',
                                               'content_type': ct})

    Permission.objects.get_or_create(codename='can_see_app_blocks',
                                     content_type__pk=ct.id,
                                     defaults={'name': 'Can see app blocks',
                                               'content_type': ct})
