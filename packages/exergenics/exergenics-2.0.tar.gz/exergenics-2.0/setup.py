from setuptools import setup, find_packages


setup(
    name='exergenics',
    version='2.0',
    author="John Christian",
    author_email='john.christian@exergenics.com',
    packages=['exergenics'],
    # package_dir={'': 'src'},
    url='https://github.com/Exergenics/internal-portal-api',
    keywords='exergenics portal api',
    install_requires=[
        'boto3',
        'datetime',
        'requests',
        'urllib3',
        'logtail-python'
    ],
)
