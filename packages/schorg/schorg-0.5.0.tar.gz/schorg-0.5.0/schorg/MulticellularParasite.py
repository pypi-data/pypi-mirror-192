"""
Multicellular parasite that causes an infection.

https://schema.org/MulticellularParasite
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class MulticellularParasiteInheritedProperties(TypedDict):
    """Multicellular parasite that causes an infection.

    References:
        https://schema.org/MulticellularParasite
    Note:
        Model Depth 6
    Attributes:
    """

    


class MulticellularParasiteProperties(TypedDict):
    """Multicellular parasite that causes an infection.

    References:
        https://schema.org/MulticellularParasite
    Note:
        Model Depth 6
    Attributes:
    """

    

#MulticellularParasiteInheritedPropertiesTd = MulticellularParasiteInheritedProperties()
#MulticellularParasitePropertiesTd = MulticellularParasiteProperties()


class AllProperties(MulticellularParasiteInheritedProperties , MulticellularParasiteProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[MulticellularParasiteProperties, MulticellularParasiteInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "MulticellularParasite"
    return model
    

MulticellularParasite = create_schema_org_model()