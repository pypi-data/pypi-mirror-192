"""
A DefinedRegion is a geographic area defined by potentially arbitrary (rather than political, administrative or natural geographical) criteria. Properties are provided for defining a region by reference to sets of postal codes.Examples: a delivery destination when shopping. Region where regional pricing is configured.Requirement 1:Country: USStates: "NY", "CA"Requirement 2:Country: USPostalCode Set: { [94000-94585], [97000, 97999], [13000, 13599]}{ [12345, 12345], [78945, 78945], }Region = state, canton, prefecture, autonomous community...

https://schema.org/DefinedRegion
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class DefinedRegionInheritedProperties(TypedDict):
    """A DefinedRegion is a geographic area defined by potentially arbitrary (rather than political, administrative or natural geographical) criteria. Properties are provided for defining a region by reference to sets of postal codes.Examples: a delivery destination when shopping. Region where regional pricing is configured.Requirement 1:Country: USStates: "NY", "CA"Requirement 2:Country: USPostalCode Set: { [94000-94585], [97000, 97999], [13000, 13599]}{ [12345, 12345], [78945, 78945], }Region = state, canton, prefecture, autonomous community...

    References:
        https://schema.org/DefinedRegion
    Note:
        Model Depth 4
    Attributes:
    """

    


class DefinedRegionProperties(TypedDict):
    """A DefinedRegion is a geographic area defined by potentially arbitrary (rather than political, administrative or natural geographical) criteria. Properties are provided for defining a region by reference to sets of postal codes.Examples: a delivery destination when shopping. Region where regional pricing is configured.Requirement 1:Country: USStates: "NY", "CA"Requirement 2:Country: USPostalCode Set: { [94000-94585], [97000, 97999], [13000, 13599]}{ [12345, 12345], [78945, 78945], }Region = state, canton, prefecture, autonomous community...

    References:
        https://schema.org/DefinedRegion
    Note:
        Model Depth 4
    Attributes:
        postalCodePrefix: (Optional[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]): A defined range of postal codes indicated by a common textual prefix. Used for non-numeric systems such as UK.
        addressCountry: (Optional[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]): The country. For example, USA. You can also provide the two-letter [ISO 3166-1 alpha-2 country code](http://en.wikipedia.org/wiki/ISO_3166-1).
        postalCodeRange: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): A defined range of postal codes.
        postalCode: (Optional[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]): The postal code. For example, 94043.
        addressRegion: (Optional[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]): The region in which the locality is, and which is in the country. For example, California or another appropriate first-level [Administrative division](https://en.wikipedia.org/wiki/List_of_administrative_divisions_by_country).
    """

    postalCodePrefix: NotRequired[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]
    addressCountry: NotRequired[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]
    postalCodeRange: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    postalCode: NotRequired[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]
    addressRegion: NotRequired[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]
    

#DefinedRegionInheritedPropertiesTd = DefinedRegionInheritedProperties()
#DefinedRegionPropertiesTd = DefinedRegionProperties()


class AllProperties(DefinedRegionInheritedProperties , DefinedRegionProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[DefinedRegionProperties, DefinedRegionInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "DefinedRegion"
    return model
    

DefinedRegion = create_schema_org_model()