"""
A nail salon.

https://schema.org/NailSalon
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class NailSalonInheritedProperties(TypedDict):
    """A nail salon.

    References:
        https://schema.org/NailSalon
    Note:
        Model Depth 5
    Attributes:
    """

    


class NailSalonProperties(TypedDict):
    """A nail salon.

    References:
        https://schema.org/NailSalon
    Note:
        Model Depth 5
    Attributes:
    """

    

#NailSalonInheritedPropertiesTd = NailSalonInheritedProperties()
#NailSalonPropertiesTd = NailSalonProperties()


class AllProperties(NailSalonInheritedProperties , NailSalonProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[NailSalonProperties, NailSalonInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "NailSalon"
    return model
    

NailSalon = create_schema_org_model()