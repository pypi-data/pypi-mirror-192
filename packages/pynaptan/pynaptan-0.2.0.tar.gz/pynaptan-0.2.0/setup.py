# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pynaptan']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.23.0,<0.24.0', 'pydantic>=1.9.1,<2.0.0', 'requests>=2.28.1,<3.0.0']

setup_kwargs = {
    'name': 'pynaptan',
    'version': '0.2.0',
    'description': 'Python package for naptan',
    'long_description': "# pynaptan\n\nA fully typed python library for retrieving UK NaPTAN stops data.\n\n## Getting started\n\nPynaptan provides a client for querying the NaPTAN data and returning the each\nstop as a `Stop` object.\n\nTo retrieve stops from NaPTAN,\n\n```python\nfrom pynaptan import Naptan\n\nclient = Naptan()\n\nistops = client.iget_all_stops()\n\n# istops is a generator\nnext(istops)\n\nStop(atco_code='0100BRP90310', naptan_code='bstgwpa', plate_code='',\ncleardown_code='', common_name='Temple Meads Stn', common_name_lang='',\nshort_common_name='Temple Meads Stn', short_common_name_lang='', landmark='',\nlandmark_lang='', street='Redcliffe Way', street_lang='', crossing='',\ncrossing_lang='', indicator='T3', indicator_lang='', bearing='SE',\nnptg_locality_code='N0077020', nptg_locality_name='Temple Meads',\nparent_locality_name='', grand_parent_locality_name='', town='', town_lang='',\nsuburb='', suburb_lang='', locality_centre=False, grid_type='UKOS', easting=359396,\nnorthing=172388, longitude=-2.58569, latitude=51.44901, stop_type='BCT',\nbus_stop_type='MKD', timing_status='OTH', default_wait_time='', notes='', notes_lang='',\nadministrative_area_code='009', creation_date_time=datetime.datetime(2009, 8, 25, 0, 0),\nmodification_date_time=datetime.datetime(2019, 9, 13, 10, 41, 24), revision_number=92,\nmodification='new', status='active')\n\n```\n\nTo retrieve all stops as a list of `Stop` objects use the `.get_all_stops` method,\n\n```python\n>> from pynaptan import Naptan\n>> client = Naptan()\n>> stops = client.get_all_stops()\n>> len(stops)\n   436167  \n```\n",
    'author': 'Ciaran McCormick',
    'author_email': 'ciaranmccormick@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/ciaranmccormick/pynaptan',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
