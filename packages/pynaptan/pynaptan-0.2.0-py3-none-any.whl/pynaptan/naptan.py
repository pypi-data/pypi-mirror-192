import csv
import os
from datetime import datetime
from io import StringIO
from logging import getLogger
from typing import Final, Iterator, List, Optional, Union

from httpx import Client, HTTPStatusError
from pydantic import BaseModel, Field, ValidationError, validator

from pynaptan.exceptions import PyNaptanError

_DEFAULT_URL: Final = "https://naptan.api.dft.gov.uk/v1/access-nodes"
NAPTAN_CSV_URL = os.environ.get("NAPTAN_CSV_URL", _DEFAULT_URL)

logger = getLogger(__name__)


class Stop(BaseModel):
    """Model for NaPTAN Stops."""

    atco_code: str = Field(..., alias="ATCOCode")
    naptan_code: str = Field(..., alias="NaptanCode")
    plate_code: str = Field(..., alias="PlateCode")
    cleardown_code: str = Field(..., alias="CleardownCode")
    common_name: str = Field(..., alias="CommonName")
    common_name_lang: str = Field(..., alias="CommonNameLang")
    short_common_name: str = Field(..., alias="ShortCommonName")
    short_common_name_lang: str = Field(..., alias="ShortCommonNameLang")
    landmark: str = Field(..., alias="Landmark")
    landmark_lang: str = Field(..., alias="LandmarkLang")
    street: str = Field(..., alias="Street")
    street_lang: str = Field(..., alias="StreetLang")
    crossing: str = Field(..., alias="Crossing")
    crossing_lang: str = Field(..., alias="CrossingLang")
    indicator: str = Field(..., alias="Indicator")
    indicator_lang: str = Field(..., alias="IndicatorLang")
    bearing: str = Field(..., alias="Bearing")
    nptg_locality_code: str = Field(..., alias="NptgLocalityCode")
    nptg_locality_name: str = Field(..., alias="LocalityName")
    parent_locality_name: str = Field(..., alias="ParentLocalityName")
    grand_parent_locality_name: str = Field(..., alias="GrandParentLocalityName")
    town: str = Field(..., alias="Town")
    town_lang: str = Field(..., alias="TownLang")
    suburb: str = Field(..., alias="Suburb")
    suburb_lang: str = Field(..., alias="SuburbLang")
    locality_centre: Optional[bool] = Field(..., alias="LocalityCentre")
    grid_type: str = Field(..., alias="GridType")
    easting: int = Field(..., alias="Easting")
    northing: int = Field(..., alias="Northing")
    longitude: Optional[float] = Field(..., alias="Longitude")
    latitude: Optional[float] = Field(..., alias="Latitude")
    stop_type: str = Field(..., alias="StopType")
    bus_stop_type: str = Field(..., alias="BusStopType")
    timing_status: str = Field(..., alias="TimingStatus")
    default_wait_time: str = Field(..., alias="DefaultWaitTime")
    notes: str = Field(..., alias="Notes")
    notes_lang: str = Field(..., alias="NotesLang")
    administrative_area_code: str = Field(..., alias="AdministrativeAreaCode")
    creation_date_time: datetime = Field(..., alias="CreationDateTime")
    modification_date_time: Optional[datetime] = Field(
        ..., alias="ModificationDateTime"
    )
    revision_number: int = Field(0, alias="RevisionNumber")
    modification: str = Field(..., alias="Modification")
    status: str = Field(..., alias="Status")

    @validator(
        "locality_centre",
        "longitude",
        "latitude",
        "modification_date_time",
        pre=True,
    )
    def handle_empty_string(cls, stop_value: str) -> Optional[str]:
        """Validate empty strings."""
        return None if stop_value == "" else stop_value

    @validator("revision_number", pre=True)
    def validate_revision_number(cls, stop_value: Union[str, int]) -> int:
        """Validate revision numbers."""
        return 0 if stop_value == "" else int(stop_value)


class Naptan(Client):
    """Class for retrieving NaPTAN Stops."""

    def __init__(self, url: str = NAPTAN_CSV_URL) -> None:
        """Initialise Naptan class."""
        super().__init__()
        self.url = url

    def get_all_stops(self) -> List[Stop]:
        """Return a list of all NaPTAN stops."""
        return list(self.iget_all_stops())

    def iget_all_stops(self) -> Iterator[Stop]:
        """Load NaPTAN Stops from the NaPTAN API."""
        api_params = {"dataFormat": "csv"}
        response = self.get(self.url, params=api_params)
        try:
            response.raise_for_status()
        except HTTPStatusError:
            raise PyNaptanError("Unable to load stops.")
        return self._iload_from_string(response.text)

    def _iload_from_string(self, csv_str: str) -> Iterator[Stop]:
        """Load NaPTAN Stops from a string representation of a csv."""
        reader = csv.DictReader(StringIO(csv_str), delimiter=",")
        for idx, entry in enumerate(reader):
            try:
                stop = Stop.parse_obj(entry)
            except ValidationError:
                logger.warn("Unable to parse row {0}, skipping.".format(idx))
                continue
            yield stop
