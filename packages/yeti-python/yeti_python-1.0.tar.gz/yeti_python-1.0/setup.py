# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyeti', 'pyeti.scripts']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.28.2,<3.0.0']

setup_kwargs = {
    'name': 'yeti-python',
    'version': '1.0',
    'description': 'Client python for YETI Platform',
    'long_description': '# pyeti-python3\nPyeti-Python (pyeti) is the bundle uses to interface with the YETI API. This is the new package that can be installed directly with pip.\nPyeti-python allows you to extract data from YETI such as specific observables (malware, IP, domains...). It can be used to plug in your own tool and enrich your Threat Intelligence feed with Yeti.\n\n## Getting Started\nTo install it you can clone the repo and run the following command:\n\n```\n$ python3 setup.py install\n```\n\nYou can also install it with pip:\n```\n$ pip3 install pyeti-python3\n``` \n\nOnce installed the first thing to do is to get your API key from the Yeti interface.\n<img src="https://raw.githubusercontent.com/fr0gger/pyeti/master/yeti_api.png">\n\nThen you can configure your script with the following information to test the connection:\n```python\nserver="<IPofYETI>"\nkey="<APIKEY>"\ntag="<NameoftheObservable>" # example: \'lokibot\'\n\napi = pyeti.YetiApi("http://%s:5000/api/" % server, api_key=key)\nrequest = api.observable_search(tags=tag, count=50)\n```\n\n## Testing\n\nYou can run tests from the root directory by running:\n\n    $ pip3 install nose\n    $ python3 setup.py test\n    \n**Note that most tests require a full running install of Yeti on localhost:5000**\n\n## Use cases\n\nFirst thing is to import the library and instantiate a client.\n\n```python\nimport pyeti, json    # json is only used for pretty printing in the examples below \napi = pyetix.YetiApi("http://localhost:5000/api/")\n```\n\nIf you are using a self signed cert on your yeti instance you can set the `verify_ssl` parameter to `True` to ignore warnings.\nOtherwise all ssl connections are verified by default.\n\n```python\nimport pyeti, json    # json is only used for pretty printing in the examples below \napi = pyeti.YetiApi("http://localhost:5000/api/", verify_ssl=False)\n```\n\n\n### Adding observables\n\n```python\nresults = api.observable_add("google.com", [\'google\'])\nprint(json.dumps(results, indent=4, sort_keys=True))\n```\n### Bulk add\n\n```python\nresults = api.observable_bulk_add(["google.com", "bing.com", "yahoo.com"])\nprint(len(results))\n3\nprint(json.dumps(results[1], indent=4, sort_keys=True))\n```\n\n### Get a single observable\n\n```python\nresults = api.observable_add("google.com")\nprint(results[\'id\'])\ninfo = api.observable_details(results[\'id\'])\nprint(json.dumps(info, indent=4, sort_keys=True))\n```\n\n### Search for observables\n\n```python\napi.observable_add("search-domain.com")\nresult = api.observable_search(value="search-dom[a-z]+", regex=True)\nprint(json.dumps(result, indent=4, sort_keys=True))\n```\n\n### Add observables\n```python\nresult = api.observable_file_add("/tmp/hello.txt", tags=[\'benign\'])\nprint(json.dumps(result, indent=4, sort_keys=True))\n# Get file contents\napi.observable_file_contents(objectid="594fff86bf365e6270f8914b")\n\'Hello!\\n\'\napi.observable_file_contents(filehash="e134ced312b3511d88943d57ccd70c83") # you can also use any hash computed above\n\'Hello!\\n\'\n```\n# License\nThis project is licensed under the Apache License - see the [LICENSE.md](https://github.com/fr0gger/pyeti/blob/master/LICENSE.md) file for details\n',
    'author': 'Sebdraven',
    'author_email': 'sebdraven@protonmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
