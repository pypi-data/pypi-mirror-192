"""
Play mode: MultiPlayer. Requiring or allowing multiple human players to play simultaneously.

https://schema.org/MultiPlayer
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class MultiPlayerInheritedProperties(TypedDict):
    """Play mode: MultiPlayer. Requiring or allowing multiple human players to play simultaneously.

    References:
        https://schema.org/MultiPlayer
    Note:
        Model Depth 5
    Attributes:
    """

    


class MultiPlayerProperties(TypedDict):
    """Play mode: MultiPlayer. Requiring or allowing multiple human players to play simultaneously.

    References:
        https://schema.org/MultiPlayer
    Note:
        Model Depth 5
    Attributes:
    """

    

#MultiPlayerInheritedPropertiesTd = MultiPlayerInheritedProperties()
#MultiPlayerPropertiesTd = MultiPlayerProperties()


class AllProperties(MultiPlayerInheritedProperties , MultiPlayerProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[MultiPlayerProperties, MultiPlayerInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "MultiPlayer"
    return model
    

MultiPlayer = create_schema_org_model()