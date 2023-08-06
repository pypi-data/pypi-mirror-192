# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['starlette_context',
 'starlette_context.middleware',
 'starlette_context.plugins']

package_data = \
{'': ['*']}

install_requires = \
['starlette']

setup_kwargs = {
    'name': 'starlette-context',
    'version': '0.3.6',
    'description': 'Middleware for Starlette that allows you to store and access the context data of a request. Can be used with logging so logs automatically use request headers such as x-request-id or x-correlation-id.',
    'long_description': '|Test Suite| |Python| |PyPI version| |codecov| |Docs| |Downloads|\n\nstarlette context\n=================\n\nMiddleware for Starlette that allows you to store and access the context\ndata of a request. Can be used with logging so logs automatically use\nrequest headers such as x-request-id or x-correlation-id.\n\nResources:\n\n-  **Source**: https://github.com/tomwojcik/starlette-context\n-  **Documentation**: https://starlette-context.readthedocs.io/\n-  **Changelog**:\n   https://starlette-context.readthedocs.io/en/latest/changelog.html\n\nInstallation\n~~~~~~~~~~~~\n\n.. code-block:: console\n\n   $ pip install starlette-context\n\nRequirements\n~~~~~~~~~~~~\n\nShould be working fine on 3.7+.\nOfficial support starts at 3.8.\n\nDependencies\n~~~~~~~~~~~~\n\n-  ``starlette``\n\nExample\n~~~~~~~\n\n.. code:: python\n\n   import uvicorn\n\n   from starlette.applications import Starlette\n   from starlette.middleware import Middleware\n   from starlette.requests import Request\n   from starlette.responses import JSONResponse\n\n   from starlette_context import context, plugins\n   from starlette_context.middleware import RawContextMiddleware\n\n   middleware = [\n       Middleware(\n           RawContextMiddleware,\n           plugins=(\n               plugins.RequestIdPlugin(),\n               plugins.CorrelationIdPlugin()\n           )\n       )\n   ]\n\n   app = Starlette(middleware=middleware)\n\n\n   @app.route("/")\n   async def index(request: Request):\n       return JSONResponse(context.data)\n\n\n   uvicorn.run(app, host="0.0.0.0")\n\nIn this example the response contains a json with\n\n.. code:: json\n\n   {\n     "X-Correlation-ID":"5ca2f0b43115461bad07ccae5976a990",\n     "X-Request-ID":"21f8d52208ec44948d152dc49a713fdd"\n   }\n\nContext can be updated and accessed at anytime if it’s created in the\nmiddleware.\n\nSponsorship\n~~~~~~~~~~~\n\nA huge thank you to `Adverity <https://www.adverity.com/>`__ for\nsponsoring the development of this OSS library in 2022.\n\nContribution\n~~~~~~~~~~~~\n\nSee the guide on `read the\ndocs <https://starlette-context.readthedocs.io/en/latest/contributing.html#contributing>`__.\n\n.. |Test Suite| image:: https://github.com/tomwojcik/starlette-context/actions/workflows/test-suite.yml/badge.svg\n   :target: https://github.com/tomwojcik/starlette-context/actions/workflows/test-suite.yml\n.. |Python| image:: https://img.shields.io/badge/python-3.8+-blue.svg\n   :target: https://www.python.org/downloads/release/python-370/\n.. |PyPI version| image:: https://badge.fury.io/py/starlette-context.svg\n   :target: https://badge.fury.io/py/starlette-context\n.. |codecov| image:: https://codecov.io/gh/tomwojcik/starlette-context/branch/master/graph/badge.svg\n   :target: https://codecov.io/gh/tomwojcik/starlette-context\n.. |Docs| image:: https://readthedocs.org/projects/pip/badge/?version=latest\n   :target: https://starlette-context.readthedocs.io/\n.. |Downloads| image:: https://img.shields.io/pypi/dm/starlette-context\n',
    'author': 'Tom Wojcik',
    'author_email': 'starlette-context-pkg@tomwojcik.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/tomwojcik/starlette-context',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
