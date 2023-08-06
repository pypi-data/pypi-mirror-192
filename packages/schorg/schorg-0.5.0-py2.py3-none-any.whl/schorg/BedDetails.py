"""
An entity holding detailed information about the available bed types, e.g. the quantity of twin beds for a hotel room. For the single case of just one bed of a certain type, you can use bed directly with a text. See also [[BedType]] (under development).

https://schema.org/BedDetails
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class BedDetailsInheritedProperties(TypedDict):
    """An entity holding detailed information about the available bed types, e.g. the quantity of twin beds for a hotel room. For the single case of just one bed of a certain type, you can use bed directly with a text. See also [[BedType]] (under development).

    References:
        https://schema.org/BedDetails
    Note:
        Model Depth 3
    Attributes:
    """

    


class BedDetailsProperties(TypedDict):
    """An entity holding detailed information about the available bed types, e.g. the quantity of twin beds for a hotel room. For the single case of just one bed of a certain type, you can use bed directly with a text. See also [[BedType]] (under development).

    References:
        https://schema.org/BedDetails
    Note:
        Model Depth 3
    Attributes:
        typeOfBed: (Optional[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]): The type of bed to which the BedDetail refers, i.e. the type of bed available in the quantity indicated by quantity.
        numberOfBeds: (Optional[Union[List[Union[SchemaOrgObj, str, StrictInt, StrictFloat]], SchemaOrgObj, str, StrictInt, StrictFloat]]): The quantity of the given bed type available in the HotelRoom, Suite, House, or Apartment.
    """

    typeOfBed: NotRequired[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]
    numberOfBeds: NotRequired[Union[List[Union[SchemaOrgObj, str, StrictInt, StrictFloat]], SchemaOrgObj, str, StrictInt, StrictFloat]]
    

#BedDetailsInheritedPropertiesTd = BedDetailsInheritedProperties()
#BedDetailsPropertiesTd = BedDetailsProperties()


class AllProperties(BedDetailsInheritedProperties , BedDetailsProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[BedDetailsProperties, BedDetailsInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "BedDetails"
    return model
    

BedDetails = create_schema_org_model()