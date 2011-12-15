from setuptools import find_packages
from setuptools import setup

setup(name='django-admin-notifications',
      version='0.1',
      description='admin notifications',
      author='Andy Baker',
      author_email='andy@andybak.net',
      packages=find_packages(),
      package_data={
          'admin_notifications': [
            'templates/*.html',
          ]
      },
      include_package_data=True,
)
