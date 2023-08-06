"""
Residence type: Single-family home.

https://schema.org/SingleFamilyResidence
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class SingleFamilyResidenceInheritedProperties(TypedDict):
    """Residence type: Single-family home.

    References:
        https://schema.org/SingleFamilyResidence
    Note:
        Model Depth 5
    Attributes:
        numberOfRooms: (Optional[Union[List[Union[SchemaOrgObj, str, StrictInt, StrictFloat]], SchemaOrgObj, str, StrictInt, StrictFloat]]): The number of rooms (excluding bathrooms and closets) of the accommodation or lodging business.Typical unit code(s): ROM for room or C62 for no unit. The type of room can be put in the unitText property of the QuantitativeValue.
    """

    numberOfRooms: NotRequired[Union[List[Union[SchemaOrgObj, str, StrictInt, StrictFloat]], SchemaOrgObj, str, StrictInt, StrictFloat]]
    


class SingleFamilyResidenceProperties(TypedDict):
    """Residence type: Single-family home.

    References:
        https://schema.org/SingleFamilyResidence
    Note:
        Model Depth 5
    Attributes:
        numberOfRooms: (Optional[Union[List[Union[SchemaOrgObj, str, StrictInt, StrictFloat]], SchemaOrgObj, str, StrictInt, StrictFloat]]): The number of rooms (excluding bathrooms and closets) of the accommodation or lodging business.Typical unit code(s): ROM for room or C62 for no unit. The type of room can be put in the unitText property of the QuantitativeValue.
        occupancy: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): The allowed total occupancy for the accommodation in persons (including infants etc). For individual accommodations, this is not necessarily the legal maximum but defines the permitted usage as per the contractual agreement (e.g. a double room used by a single person).Typical unit code(s): C62 for person
    """

    numberOfRooms: NotRequired[Union[List[Union[SchemaOrgObj, str, StrictInt, StrictFloat]], SchemaOrgObj, str, StrictInt, StrictFloat]]
    occupancy: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    

#SingleFamilyResidenceInheritedPropertiesTd = SingleFamilyResidenceInheritedProperties()
#SingleFamilyResidencePropertiesTd = SingleFamilyResidenceProperties()


class AllProperties(SingleFamilyResidenceInheritedProperties , SingleFamilyResidenceProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[SingleFamilyResidenceProperties, SingleFamilyResidenceInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "SingleFamilyResidence"
    return model
    

SingleFamilyResidence = create_schema_org_model()