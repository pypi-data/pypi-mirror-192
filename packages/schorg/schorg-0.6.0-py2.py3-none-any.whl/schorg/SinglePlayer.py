"""
Play mode: SinglePlayer. Which is played by a lone player.

https://schema.org/SinglePlayer
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class SinglePlayerInheritedProperties(TypedDict):
    """Play mode: SinglePlayer. Which is played by a lone player.

    References:
        https://schema.org/SinglePlayer
    Note:
        Model Depth 5
    Attributes:
    """

    


class SinglePlayerProperties(TypedDict):
    """Play mode: SinglePlayer. Which is played by a lone player.

    References:
        https://schema.org/SinglePlayer
    Note:
        Model Depth 5
    Attributes:
    """

    

#SinglePlayerInheritedPropertiesTd = SinglePlayerInheritedProperties()
#SinglePlayerPropertiesTd = SinglePlayerProperties()


class AllProperties(SinglePlayerInheritedProperties , SinglePlayerProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[SinglePlayerProperties, SinglePlayerInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "SinglePlayer"
    return model
    

SinglePlayer = create_schema_org_model()