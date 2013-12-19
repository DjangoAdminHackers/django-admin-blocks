from setuptools import find_packages
from setuptools import setup

setup(name='django-admin-blocks',
      version='0.1',
      description='admin blocks',
      author='Andy Baker',
      author_email='andy@andybak.net',
      packages=find_packages(),
      package_data={
          'django_admin_blocks': [
            'templates/*.html',
          ]
      },
      include_package_data=True,
)
