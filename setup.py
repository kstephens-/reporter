from setuptools import setup

## dependencies
# geoip2
# py.test
requires = [
    'geoip2 == 2.4.2'
]

setup(
    name='reporter',
    version='0.0',
    description='country and state reports for apache access logs',
    packages=['reporter'],
    install_requires=requires,
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    scripts=['bin/access-report'],
    include_package_data=True,
    zip_safe=False
)
