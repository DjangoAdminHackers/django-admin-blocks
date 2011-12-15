from optparse import make_option

from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--group', '-g', default=None, dest='group',
            help='The group name to assign the permissions'),
    )

    help = "Clean unused images"
    def handle(self, *args, **options):
        from admin_notifications.models import create_app_permissions
        group_name = options.get('group')

        print 'Creating admin notifications Permissions'
        create_app_permissions('a')

        print 'Assigning the permission to group "%s"' % group_name
        try:
            group = Group.objects.get(name=group_name)
        except:
            print 'Group "%s" cannot be found. ' % group_name
            return

        error_perm = Permission.objects.get(codename='can_see_error_notifications',)
        app_perm = Permission.objects.get(codename='can_see_app_blocks',)
        group.permissions.add(error_perm, app_perm)

        print '=' * 30, 'done!', '=' * 30

