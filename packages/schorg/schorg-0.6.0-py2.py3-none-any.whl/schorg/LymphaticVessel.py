"""
A type of blood vessel that specifically carries lymph fluid unidirectionally toward the heart.

https://schema.org/LymphaticVessel
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class LymphaticVesselInheritedProperties(TypedDict):
    """A type of blood vessel that specifically carries lymph fluid unidirectionally toward the heart.

    References:
        https://schema.org/LymphaticVessel
    Note:
        Model Depth 5
    Attributes:
    """

    


class LymphaticVesselProperties(TypedDict):
    """A type of blood vessel that specifically carries lymph fluid unidirectionally toward the heart.

    References:
        https://schema.org/LymphaticVessel
    Note:
        Model Depth 5
    Attributes:
        regionDrained: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): The anatomical or organ system drained by this vessel; generally refers to a specific part of an organ.
        originatesFrom: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): The vasculature the lymphatic structure originates, or afferents, from.
        runsTo: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): The vasculature the lymphatic structure runs, or efferents, to.
    """

    regionDrained: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    originatesFrom: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    runsTo: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    

#LymphaticVesselInheritedPropertiesTd = LymphaticVesselInheritedProperties()
#LymphaticVesselPropertiesTd = LymphaticVesselProperties()


class AllProperties(LymphaticVesselInheritedProperties , LymphaticVesselProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[LymphaticVesselProperties, LymphaticVesselInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "LymphaticVessel"
    return model
    

LymphaticVessel = create_schema_org_model()