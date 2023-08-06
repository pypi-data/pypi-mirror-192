"""
The geographic coordinates of a place or event.

https://schema.org/GeoCoordinates
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class GeoCoordinatesInheritedProperties(TypedDict):
    """The geographic coordinates of a place or event.

    References:
        https://schema.org/GeoCoordinates
    Note:
        Model Depth 4
    Attributes:
    """

    


class GeoCoordinatesProperties(TypedDict):
    """The geographic coordinates of a place or event.

    References:
        https://schema.org/GeoCoordinates
    Note:
        Model Depth 4
    Attributes:
        longitude: (Optional[Union[List[Union[SchemaOrgObj, str, StrictInt, StrictFloat]], SchemaOrgObj, str, StrictInt, StrictFloat]]): The longitude of a location. For example ```-122.08585``` ([WGS 84](https://en.wikipedia.org/wiki/World_Geodetic_System)).
        elevation: (Optional[Union[List[Union[SchemaOrgObj, str, StrictInt, StrictFloat]], SchemaOrgObj, str, StrictInt, StrictFloat]]): The elevation of a location ([WGS 84](https://en.wikipedia.org/wiki/World_Geodetic_System)). Values may be of the form 'NUMBER UNIT\_OF\_MEASUREMENT' (e.g., '1,000 m', '3,200 ft') while numbers alone should be assumed to be a value in meters.
        addressCountry: (Optional[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]): The country. For example, USA. You can also provide the two-letter [ISO 3166-1 alpha-2 country code](http://en.wikipedia.org/wiki/ISO_3166-1).
        postalCode: (Optional[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]): The postal code. For example, 94043.
        address: (Optional[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]): Physical address of the item.
        latitude: (Optional[Union[List[Union[SchemaOrgObj, str, StrictInt, StrictFloat]], SchemaOrgObj, str, StrictInt, StrictFloat]]): The latitude of a location. For example ```37.42242``` ([WGS 84](https://en.wikipedia.org/wiki/World_Geodetic_System)).
    """

    longitude: NotRequired[Union[List[Union[SchemaOrgObj, str, StrictInt, StrictFloat]], SchemaOrgObj, str, StrictInt, StrictFloat]]
    elevation: NotRequired[Union[List[Union[SchemaOrgObj, str, StrictInt, StrictFloat]], SchemaOrgObj, str, StrictInt, StrictFloat]]
    addressCountry: NotRequired[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]
    postalCode: NotRequired[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]
    address: NotRequired[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]
    latitude: NotRequired[Union[List[Union[SchemaOrgObj, str, StrictInt, StrictFloat]], SchemaOrgObj, str, StrictInt, StrictFloat]]
    

#GeoCoordinatesInheritedPropertiesTd = GeoCoordinatesInheritedProperties()
#GeoCoordinatesPropertiesTd = GeoCoordinatesProperties()


class AllProperties(GeoCoordinatesInheritedProperties , GeoCoordinatesProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[GeoCoordinatesProperties, GeoCoordinatesInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "GeoCoordinates"
    return model
    

GeoCoordinates = create_schema_org_model()