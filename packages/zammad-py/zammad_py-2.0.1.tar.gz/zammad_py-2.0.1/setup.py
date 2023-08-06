# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['zammad_py']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.25.1,<3.0.0']

setup_kwargs = {
    'name': 'zammad-py',
    'version': '2.0.1',
    'description': 'Python API client for zammad',
    'long_description': '=================\nZammad API Client\n=================\n\n\n.. image:: https://img.shields.io/pypi/v/zammad_py.svg\n        :target: https://pypi.python.org/pypi/zammad_py\n\n.. image:: https://img.shields.io/travis/joeirimpan/zammad_py.svg\n        :target: https://travis-ci.org/joeirimpan/zammad_py\n\n.. image:: https://readthedocs.org/projects/zammad-py/badge/?version=latest\n        :target: https://zammad-py.readthedocs.io/en/latest/?badge=latest\n        :alt: Documentation Status\n\n.. image:: https://pyup.io/repos/github/joeirimpan/zammad_py/shield.svg\n     :target: https://pyup.io/repos/github/joeirimpan/zammad_py/\n     :alt: Updates\n\n\nPython API client for zammad\n\n* Free software: MIT license\n* Documentation: https://zammad-py.readthedocs.io.\n\n\nQuickstart\n----------\n\n\n.. code-block:: python\n\n    from zammad_py import ZammadAPI\n\n    # Initialize the client with the URL, username, and password\n    client = ZammadAPI(url=\'<HOST>\', username=\'<USERNAME>\', password=\'<PASSWORD>\')\n\n    # Example: Access all users\n    this_page = client.user.all()\n    for user in this_page:\n        print(user)\n\n    # Example: Get information about the current user\n    print(client.user.me())\n\n    # Example: Create a ticket\n    params = {\n       "title": "Help me!",\n       "group": "2nd Level",\n       "customer": "david@example.com",\n       "article": {\n          "subject": "My subject",\n          "body": "I am a message!",\n          "type": "note",\n          "internal": false\n       }\n    }\n    new_ticket = client.ticket.create(params=params)\n\n\n\nGeneral Methods\n---------------\nMost resources support these methods:\n\n.all(): Returns a paginated response with the current page number and a list of elements.\n\n.next_page(): Returns the next page of the current pagination object.\n\n.prev_page(): Returns the previous page of the current pagination object.\n\n.search(params): Returns a paginated response based on the search parameters.\n\n.find(id): Returns a single object with the specified ID.\n\n.create(params): Creates a new object with the specified parameters.\n\n.update(params): Updates an existing object with the specified parameters.\n\n.destroy(id): Deletes an object with the specified ID.\n\nAdditional Resource Methods\n---------------------------\nUser resource also has the .me() method to get information about the current user.\n\nTicket resource also has the .articles() method to get the articles associated with a ticket.\n\nLink resource has methods to list, add, and delete links between objects.\n\nTicketArticleAttachment resource has the .download() method to download a ticket attachment.\n\nObject resource has the .execute_migrations() method to run migrations on an object.\n\nContributing\n------------\nThe Zammad API Client (zammad_py) welcomes contributions.\n\nYou can contribute by reporting bugs, fixing bugs, implementing new features, writing documentation, and submitting feedback.\n\nTo get started, see the contributing section in the docs!\n\nPlease ensure that your changes include tests and updated documentation if necessary.\n\nCredits\n-------\n\nThis package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.\n\n.. _Cookiecutter: https://github.com/audreyr/cookiecutter\n.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage\n\n',
    'author': 'Joe Paul',
    'author_email': 'joeirimpan@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/joeirimpan/zammad_py',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.1,<4.0',
}


setup(**setup_kwargs)
