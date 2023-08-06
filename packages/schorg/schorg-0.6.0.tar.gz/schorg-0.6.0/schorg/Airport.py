"""
An airport.

https://schema.org/Airport
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class AirportInheritedProperties(TypedDict):
    """An airport.

    References:
        https://schema.org/Airport
    Note:
        Model Depth 4
    Attributes:
        openingHours: (Optional[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]): The general opening hours for a business. Opening hours can be specified as a weekly time range, starting with days, then times per day. Multiple days can be listed with commas ',' separating each day. Day or time ranges are specified using a hyphen '-'.* Days are specified using the following two-letter combinations: ```Mo```, ```Tu```, ```We```, ```Th```, ```Fr```, ```Sa```, ```Su```.* Times are specified using 24:00 format. For example, 3pm is specified as ```15:00```, 10am as ```10:00```. * Here is an example: <code>&lt;time itemprop="openingHours" datetime=&quot;Tu,Th 16:00-20:00&quot;&gt;Tuesdays and Thursdays 4-8pm&lt;/time&gt;</code>.* If a business is open 7 days a week, then it can be specified as <code>&lt;time itemprop=&quot;openingHours&quot; datetime=&quot;Mo-Su&quot;&gt;Monday through Sunday, all day&lt;/time&gt;</code>.
    """

    openingHours: NotRequired[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]
    


class AirportProperties(TypedDict):
    """An airport.

    References:
        https://schema.org/Airport
    Note:
        Model Depth 4
    Attributes:
        iataCode: (Optional[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]): IATA identifier for an airline or airport.
        icaoCode: (Optional[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]): ICAO identifier for an airport.
    """

    iataCode: NotRequired[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]
    icaoCode: NotRequired[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]
    

#AirportInheritedPropertiesTd = AirportInheritedProperties()
#AirportPropertiesTd = AirportProperties()


class AllProperties(AirportInheritedProperties , AirportProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[AirportProperties, AirportInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "Airport"
    return model
    

Airport = create_schema_org_model()