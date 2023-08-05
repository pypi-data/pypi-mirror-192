import csv
import os
import zipfile
from datetime import datetime
from functools import cached_property
from io import BytesIO, StringIO
from logging import getLogger
from typing import List

from httpx import Client, HTTPStatusError
from pydantic import BaseModel, Field

from pynaptan.exceptions import PyNaptanError

logger = getLogger(__name__)

NPTG_URL = os.environ.get(
    "NPTG_URL", "https://naptan.app.dft.gov.uk/datarequest/nptg.ashx"
)


class NPTGBaseModel(BaseModel):
    """BaseModel for all NPTG models."""

    creation_date_time: datetime = Field(..., alias="CreationDateTime")
    revision_number: int = Field(..., alias="RevisionNumber")
    modification_date_time: datetime = Field(..., alias="ModificationDateTime")
    modification: str = Field("", alias="Modification")


class Region(NPTGBaseModel):
    """Model for Region."""

    region_code: str = Field(..., alias="RegionCode")
    region_name: str = Field(..., alias="RegionName")
    region_name_lang: str = Field(..., alias="RegionNameLang")


class AdminArea(NPTGBaseModel):
    """Model for Admin Areas."""

    administrative_area_code: int = Field(..., alias="AdministrativeAreaCode")
    atco_area_code: int = Field(..., alias="AtcoAreaCode")
    area_name: str = Field(..., alias="AreaName")
    area_name_lang: str = Field("", alias="AreaNameLang")
    short_name: str = Field(..., alias="ShortName")
    short_name_lang: str = Field("", alias="ShortNameLang")
    country: str = Field(..., alias="Country")
    region_code: str = Field(..., alias="RegionCode")
    maximum_length_for_short_name: str = Field("", alias="MaximumLengthForShortNames")
    national: int = Field(..., alias="National")
    contact_email: str = Field("", alias="ContactEmail")
    contact_telephone: str = Field("", alias="ContactTelephone")


class District(NPTGBaseModel):
    """Model for Districts."""

    district_code: str = Field(..., alias="DistrictCode")
    district_name: str = Field(..., alias="DistrictName")
    district_lang: str = Field("", alias="DistrictNameLang")
    administrative_area_code: int = Field(..., alias="AdministrativeAreaCode")


class Locality(NPTGBaseModel):
    """Model for Localities."""

    nptg_locality_code: str = Field(..., alias="NptgLocalityCode")
    locality_name: str = Field(..., alias="LocalityName")
    locality_name_lang: str = Field(..., alias="LocalityNameLang")
    short_name: str = Field(..., alias="ShortName")
    short_name_lang: str = Field("", alias="ShortNameLang")
    qualifier_name: str = Field("", alias="QualifierName")
    qualifier_name_lang: str = Field("", alias="QualifierNameLang")
    qualifier_locality_ref: str = Field("", alias="QualifierLocalityRef")
    qualifier_district_ref: str = Field("", alias="QualifierDistrictRef")
    administrative_area_code: int = Field(..., alias="AdministrativeAreaCode")
    nptg_district_code: int = Field(..., alias="NptgDistrictCode")
    source_locality_type: str = Field(..., alias="SourceLocalityType")
    grid_type: str = Field(..., alias="GridType")
    easting: int = Field(..., alias="Easting")
    northing: int = Field(..., alias="Northing")


class NPTGClient(Client):
    """A client for requesting NPTG data."""

    def get_zipdata(self, url: str = NPTG_URL) -> bytes:
        """Get NPTG zipdata from the website."""
        query_params = {"format": "csv"}
        logger.debug("Getting the data from NPTG.")
        response = self.get(url, params=query_params)
        try:
            response.raise_for_status()
        except HTTPStatusError:
            raise PyNaptanError("Unable to fetch NPTG data.")
        return response.content


class NPTG:
    """Class for retrieving NPTG data."""

    def __init__(self, client: NPTGClient):
        """Client for retrieving NPTGClient data."""
        self._client = client

    @cached_property
    def zipdata(self) -> BytesIO:
        """NPTG zip data."""
        return BytesIO(self._client.get_zipdata())

    def get_regions(self) -> List[Region]:
        """Get all the NPTG regions."""
        filename = "Regions.csv"
        csvfile = self._extract_file(filename)
        reader = csv.DictReader(csvfile)
        return [Region.parse_obj(region) for region in reader]

    def get_admin_areas(self) -> List[AdminArea]:
        """Get all the NPTG admin areas."""
        filename = "AdminAreas.csv"
        csvfile = self._extract_file(filename)
        reader = csv.DictReader(csvfile)
        return [AdminArea.parse_obj(area) for area in reader]

    def get_districts(self) -> List[District]:
        """Get all the NPTG districts."""
        filename = "Districts.csv"
        csvfile = self._extract_file(filename)
        reader = csv.DictReader(csvfile)
        return [District.parse_obj(district) for district in reader]

    def get_localities(self) -> List[Locality]:
        """Get all the NPTG localities."""
        filename = "Localities.csv"
        csvfile = self._extract_file(filename)
        reader = csv.DictReader(csvfile)
        return [Locality.parse_obj(locality) for locality in reader]

    def _extract_file(self, filename: str) -> StringIO:
        """Extract a specific file from the NPTG zipfile."""
        with zipfile.ZipFile(self.zipdata) as nptg:
            with nptg.open(filename) as csvfile:
                return StringIO(csvfile.read().decode("UTF-8"))
