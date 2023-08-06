# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['django_socio_grpc',
 'django_socio_grpc.grpc_actions',
 'django_socio_grpc.management',
 'django_socio_grpc.management.commands',
 'django_socio_grpc.protobuf',
 'django_socio_grpc.protobuf.protoparser',
 'django_socio_grpc.protobuf.tests',
 'django_socio_grpc.protobuf.tests.protos',
 'django_socio_grpc.request_transformer',
 'django_socio_grpc.services',
 'django_socio_grpc.tests',
 'django_socio_grpc.tests.assets',
 'django_socio_grpc.tests.fakeapp',
 'django_socio_grpc.tests.fakeapp.grpc',
 'django_socio_grpc.tests.fakeapp.migrations',
 'django_socio_grpc.tests.fakeapp.services',
 'django_socio_grpc.tests.grpc_test_utils',
 'django_socio_grpc.utils']

package_data = \
{'': ['*'],
 'django_socio_grpc.tests': ['protos/ALL_APP_GENERATED_NO_SEPARATE/*',
                             'protos/ALL_APP_GENERATED_SEPARATE/*',
                             'protos/CUSTOM_APP_MODEL_GENERATED/*',
                             'protos/MODEL_WITH_KNOWN_METHOD_OVERRIDEN_GENERATED/*',
                             'protos/MODEL_WITH_M2M_GENERATED/*',
                             'protos/MODEL_WITH_STRUCT_IMORT_IN_ARRAY/*',
                             'protos/NO_MODEL_GENERATED/*',
                             'protos/SIMPLE_APP_MODEL_GENERATED_FROM_OLD_ORDER/*',
                             'protos/SIMPLE_APP_MODEL_OLD_ORDER/*',
                             'protos/SIMPLE_MODEL_GENERATED/*']}

install_requires = \
['asyncio>=3.4.3,<4.0.0',
 'django>=2.2',
 'djangorestframework',
 'grpcio-tools>=1.50.0,<2.0.0',
 'grpcio>=1.50.0,<2.0.0',
 'proto-parser>=1.6.3,<2.0.0']

entry_points = \
{'console_scripts': ['tests = test_utils.load_tests:launch']}

setup_kwargs = {
    'name': 'django-socio-grpc',
    'version': '0.18.0rc7',
    'description': 'Fork of django-grpc-framework with more feature maintained by the socio team. Make GRPC with django easy.',
    'long_description': 'None',
    'author': 'Adrien Montagu',
    'author_email': 'adrienmontagu@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
