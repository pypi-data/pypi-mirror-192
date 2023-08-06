# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bayesianpia2']

package_data = \
{'': ['*']}

install_requires = \
['python-semantic-release>=7.33.1,<8.0.0', 'semver>=2.13.0,<3.0.0']

setup_kwargs = {
    'name': 'bayesianpia2',
    'version': '0.0.4',
    'description': '',
    'long_description': '# Lab 2 IA\n\n__init__(self, nodes, edges): el constructor de la clase. Recibe una lista de nodos y un diccionario de bordes, donde las claves son los nombres de los nodos y los valores son listas de los nombres de los nodos padre. \n\nis_fully_described(self): comprueba si se han definido los factores de probabilidad de todos los nodos de la red. Devuelve true si estoe es cierto y false si no \n\ncompact(self): devuelve una cadena que representa la red bayesiana de forma compacta. \n\n\nrepresentation(self): devuelve una cadena que representa la red bayesiana de forma detallada. Incluye la tabla de probabilidad de cada nodo dada la probabilidad condicional de sus padres.\n\ncompute_factor(self, node, evidence={}): calcula el factor de probabilidad del nodo node dado un diccionario de evidencia. \n\ncompute_conditional_probability(self, node, parent_state): calcula la probabilidad condicional del nodo node dada la evidencia en el diccionario parent_state.',
    'author': 'IPablo271',
    'author_email': '69815580+IPablo271@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
