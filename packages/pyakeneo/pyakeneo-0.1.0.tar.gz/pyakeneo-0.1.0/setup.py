# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyakeneo']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.28.2,<3.0.0', 'structlog>=22.3.0,<23.0.0']

setup_kwargs = {
    'name': 'pyakeneo',
    'version': '0.1.0',
    'description': 'Python client for the Akeneo API REST',
    'long_description': '|Build Status|\n|Documentation Status|\n\n\nPython client for Akeneo PIM API\n================================\n\nA simple Python client to use the `Akeneo PIM API`_.\n\nDependencies are managed with `pipenv`_\n(list of dependencies available in `Pipfile`_).\n\n.. _Pipfile: Pipfile\n\nYou may install them with:\n\n.. code:: bash\n\n        pipenv install --dev\n\nInstallation\n------------\nThe easiest is to use pipenv in your new project:\n\n.. code:: bash\n\n        pipenv install git+https://github.com/matthieudelaro/akeneo_api_client#egg=akeneo_api_client\n        \nUsage\n-----\n\nA simple example is provided in `docs/example.py`_.\n\n.. _docs/example.py: https://raw.githubusercontent.com/matthieudelaro/akeneo_api_client/master/docs/example.py\n\nTo export the data from your PIM, you may use the `docs/example_exporter.py`_.\n\nIf you experience issues when importing modules, run the examples as follow:\n\n.. code:: bash\n\n        cd docs\n        pipenv run python3 example_exporter.py\n        \n\n.. _docs/example_exporter.py: https://raw.githubusercontent.com/matthieudelaro/akeneo_api_client/master/docs/example_exporter.py\n\nTests\n-----\n\nRun tests as follow:\n\n.. code:: bash\n\n        pipenv run nosetests\n        \nIf tests don\'t pass in your environment, please check that dependencies match those described in Pipfile. One way to do it is to ensure that pipenv runs commands in a dedicated virtualenv by setting environment variable as follow:\n\n.. code:: bash\n\n        export PIPENV_IGNORE_VIRTUALENVS=1\n        pipenv install --dev  # (re)run installation of dependencies\n\nOr even emulate Travis in Docker:\n\n.. code:: bash\n\n        # This will: \n        # - copy the current directory into a temporary directory, which will be mounted in (and modified by) a docker container\n        # - run the container of Travis as explained here: https://stackoverflow.com/a/49019950\n        # - run the steps of Travis thanks to wwtd: https://github.com/grosser/wwtd\n        rm -rf /tmp/localTravis; cp -R . /tmp/localTravis; INSTANCE="travisci/ci-garnet:packer-1512502276-986baf0"; BUILDID="build-$RANDOM"; docker run --name $BUILDID -dit -v /tmp/localTravis:/home/travis/matthieudelaro/akeneo_api_client $INSTANCE /sbin/init; docker exec -it --user travis $BUILDID bash -lc "whoami; cd /home/travis/matthieudelaro/akeneo_api_client; gem install wwtd; source ~/virtualenv/python3.6/bin/activate; wwtd -u before_install -u install -u before_script -u language -u python; history; bash"\n\n\nTests are provided with mocks, recorded with `VCR.py`_. In case you need\nto (re)run tests, you should install the dataset in you PIM instance as\nfollow:\n\n- specify the database to install in app/config/parameters.yml:\n\n.. code:: yaml\n\n        installer_data: PimInstallerBundle:icecat_demo_dev\n\n-  install the database by running the following command:\n\n   .. code:: bash\n\n       bin/console pim:installer:db --env=prod\n       # or, in case you are using Docker:\n       docker-compose exec fpm bin/console pim:installer:db --env=prod\n\n.. _Akeneo PIM API: https://api.akeneo.com/\n.. _pipenv: https://github.com/kennethreitz/pipenv\n.. _VCR.py: http://vcrpy.readthedocs.io/en/latest/index.html\n\n.. |Build Status| image:: https://travis-ci.org/matthieudelaro/akeneo_api_client.svg?branch=master\n   :target: https://travis-ci.org/matthieudelaro/akeneo_api_client\n.. |Documentation Status| image:: https://readthedocs.org/projects/akeneo-api-client/badge/?version=latest\n   :target: http://akeneo-api-client.readthedocs.io/en/latest/\n',
    'author': 'Kave Tech',
    'author_email': 'kavetech@kavehome.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
