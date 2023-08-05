# pynaptan

A fully typed python library for retrieving UK NaPTAN stops data.

## Getting started

Pynaptan provides a client for querying the NaPTAN data and returning the each
stop as a `Stop` object.

To retrieve stops from NaPTAN,

```python
from pynaptan import Naptan

client = Naptan()

istops = client.iget_all_stops()

# istops is a generator
next(istops)

Stop(atco_code='0100BRP90310', naptan_code='bstgwpa', plate_code='',
cleardown_code='', common_name='Temple Meads Stn', common_name_lang='',
short_common_name='Temple Meads Stn', short_common_name_lang='', landmark='',
landmark_lang='', street='Redcliffe Way', street_lang='', crossing='',
crossing_lang='', indicator='T3', indicator_lang='', bearing='SE',
nptg_locality_code='N0077020', nptg_locality_name='Temple Meads',
parent_locality_name='', grand_parent_locality_name='', town='', town_lang='',
suburb='', suburb_lang='', locality_centre=False, grid_type='UKOS', easting=359396,
northing=172388, longitude=-2.58569, latitude=51.44901, stop_type='BCT',
bus_stop_type='MKD', timing_status='OTH', default_wait_time='', notes='', notes_lang='',
administrative_area_code='009', creation_date_time=datetime.datetime(2009, 8, 25, 0, 0),
modification_date_time=datetime.datetime(2019, 9, 13, 10, 41, 24), revision_number=92,
modification='new', status='active')

```

To retrieve all stops as a list of `Stop` objects use the `.get_all_stops` method,

```python
>> from pynaptan import Naptan
>> client = Naptan()
>> stops = client.get_all_stops()
>> len(stops)
   436167  
```
