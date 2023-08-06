"""
A dance group&#x2014;for example, the Alvin Ailey Dance Theater or Riverdance.

https://schema.org/DanceGroup
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class DanceGroupInheritedProperties(TypedDict):
    """A dance group&#x2014;for example, the Alvin Ailey Dance Theater or Riverdance.

    References:
        https://schema.org/DanceGroup
    Note:
        Model Depth 4
    Attributes:
    """

    


class DanceGroupProperties(TypedDict):
    """A dance group&#x2014;for example, the Alvin Ailey Dance Theater or Riverdance.

    References:
        https://schema.org/DanceGroup
    Note:
        Model Depth 4
    Attributes:
    """

    

#DanceGroupInheritedPropertiesTd = DanceGroupInheritedProperties()
#DanceGroupPropertiesTd = DanceGroupProperties()


class AllProperties(DanceGroupInheritedProperties , DanceGroupProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[DanceGroupProperties, DanceGroupInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "DanceGroup"
    return model
    

DanceGroup = create_schema_org_model()