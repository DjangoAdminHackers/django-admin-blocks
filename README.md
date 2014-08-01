django-admin-blocks
===================

django-admin-blocks


Very quick readme :)


Rather than painfully deal with multiple apps that all want to override admin templates but clash with each other, this app aims to give you an easy 'autodiscovery' style way to define (currently) 3 common types of admin template customizations.

1.  Add a file called 'admin_blocks.py' to any app in INSTALLED apps. The format for this will be explained shortly.
2. In your urls.py import django_admin_blocks and then call django_admin_blocks.autodiscover()
3. Add each of the three template tags to the appropriate custom admin template.

You'll need {% load admin_blocks_tags %} in any of your custom admin templates you want to insert blocks into.

Nothing directly related to this app but we highly recommend using the django-apptemplates loader if you're customizing admin templates: https://bitbucket.org/tzulberti/django-apptemplates/

Sample admin_blocks.py
----------------------

    import django_admin_blocks
    from linkcheck.models import Link

    def broken_links():
        broken_links = Link.objects.filter(ignore=False, url__status=False).count()
        if broken_links:
            return "You have %s broken link." % broken_links)

    def notify_take_deposit():
        "Deposit Due"
        bookings = get_notify_deposit_bookings()
        return render_to_string('tag_notify_take_deposit.html', {'bookings':bookings})
        
    def linkcheck_app_block():
        return "<a href='%s'>Link Checker</a>" % reverse('linkchecker') 

    def filebrowser_app_block():
        return "<a href='%s'>File Browser</a>" % reverse('filebrowser:fb_browse')
    
    django_admin_blocks.register({
        'errors': (
             broken_links,
        ),
        'app_blocks': [
            ("Utils", notify_take_deposit),
            ("Bookings", filebrowser_app_block, linkcheck_app_block),
        ],
        'script_blocks': [
            {'url_path': 'js/admin_sortable/jquery-ui-1.10.3.custom.min.js'},
            {'url_path': 'js/admin_sortable/admin_sortable.js'},
        ],
    })


The tags
========

{% script_block %}
------------------

Add this tag after existing script tags in your base admin template.


{% error_blocks %}
------------------

Add this just inside {% block content %} in your index template (or base template if you want errors shown on all pages)


{% app_block app %}
------------------

This allows you to add blocks to each app's section of the admin index page. It needs to be placed just after the {% for model in app.models %} loop and before the following closing table tag:

    {% endfor %}
    {% app_block app %}
    </table>
