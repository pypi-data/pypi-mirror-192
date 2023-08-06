# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['volumetricspy', 'volumetricspy.stats', 'volumetricspy.utils']

package_data = \
{'': ['*']}

install_requires = \
['Shapely>=1.7.1,<2.0.0',
 'folium==0.13.0',
 'geopandas>=0.10.2,<0.11.0',
 'mapclassify>=2.4.3,<3.0.0',
 'matplotlib>=3.4.3,<4.0.0',
 'numpy>=1.21.2,<2.0.0',
 'pandas>=1.3.2,<2.0.0',
 'plotly>=5.10.0,<6.0.0',
 'pydantic>=1.8.2,<2.0.0',
 'pyvista>=0.31.3,<0.32.0',
 'scikit-image>=0.18.2,<0.19.0',
 'scipy>=1.7.1,<2.0.0',
 'seaborn>=0.11.2,<0.12.0',
 'zmapio>=0.6.0,<0.7.0']

setup_kwargs = {
    'name': 'volumetricspy',
    'version': '0.1.10',
    'description': 'Oil & Gas Tool for estimating Original in Place Resources',
    'long_description': 'None',
    'author': 'Santiago Cuervo',
    'author_email': 'scuervo91@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
