"""
A winery.

https://schema.org/Winery
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class WineryInheritedProperties(TypedDict):
    """A winery.

    References:
        https://schema.org/Winery
    Note:
        Model Depth 5
    Attributes:
        starRating: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): An official rating for a lodging business or food establishment, e.g. from national associations or standards bodies. Use the author property to indicate the rating organization, e.g. as an Organization with name such as (e.g. HOTREC, DEHOGA, WHR, or Hotelstars).
        servesCuisine: (Optional[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]): The cuisine of the restaurant.
        acceptsReservations: (Optional[Union[List[Union[StrictBool, SchemaOrgObj, str, AnyUrl]], StrictBool, SchemaOrgObj, str, AnyUrl]]): Indicates whether a FoodEstablishment accepts reservations. Values can be Boolean, an URL at which reservations can be made or (for backwards compatibility) the strings ```Yes``` or ```No```.
        menu: (Optional[Union[List[Union[SchemaOrgObj, str, AnyUrl]], SchemaOrgObj, str, AnyUrl]]): Either the actual menu as a structured representation, as text, or a URL of the menu.
        hasMenu: (Optional[Union[List[Union[SchemaOrgObj, str, AnyUrl]], SchemaOrgObj, str, AnyUrl]]): Either the actual menu as a structured representation, as text, or a URL of the menu.
    """

    starRating: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    servesCuisine: NotRequired[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]
    acceptsReservations: NotRequired[Union[List[Union[StrictBool, SchemaOrgObj, str, AnyUrl]], StrictBool, SchemaOrgObj, str, AnyUrl]]
    menu: NotRequired[Union[List[Union[SchemaOrgObj, str, AnyUrl]], SchemaOrgObj, str, AnyUrl]]
    hasMenu: NotRequired[Union[List[Union[SchemaOrgObj, str, AnyUrl]], SchemaOrgObj, str, AnyUrl]]
    


class WineryProperties(TypedDict):
    """A winery.

    References:
        https://schema.org/Winery
    Note:
        Model Depth 5
    Attributes:
    """

    

#WineryInheritedPropertiesTd = WineryInheritedProperties()
#WineryPropertiesTd = WineryProperties()


class AllProperties(WineryInheritedProperties , WineryProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[WineryProperties, WineryInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "Winery"
    return model
    

Winery = create_schema_org_model()