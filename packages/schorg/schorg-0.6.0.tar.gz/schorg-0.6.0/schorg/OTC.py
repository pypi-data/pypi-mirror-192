"""
The character of a medical substance, typically a medicine, of being available over the counter or not.

https://schema.org/OTC
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class OTCInheritedProperties(TypedDict):
    """The character of a medical substance, typically a medicine, of being available over the counter or not.

    References:
        https://schema.org/OTC
    Note:
        Model Depth 6
    Attributes:
    """

    


class OTCProperties(TypedDict):
    """The character of a medical substance, typically a medicine, of being available over the counter or not.

    References:
        https://schema.org/OTC
    Note:
        Model Depth 6
    Attributes:
    """

    

#OTCInheritedPropertiesTd = OTCInheritedProperties()
#OTCPropertiesTd = OTCProperties()


class AllProperties(OTCInheritedProperties , OTCProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[OTCProperties, OTCInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "OTC"
    return model
    

OTC = create_schema_org_model()